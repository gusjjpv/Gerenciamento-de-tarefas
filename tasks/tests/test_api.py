"""Testes da API REST do app tasks (/projetos/ e /tarefas/)."""

import pytest

from tasks.models import Projeto, Tarefa

pytestmark = pytest.mark.django_db

PROJETOS_URL = "/projetos/"
TAREFAS_URL = "/tarefas/"


def projeto_url(pk):
    return f"{PROJETOS_URL}{pk}/"


def tarefa_url(pk):
    return f"{TAREFAS_URL}{pk}/"


# --------------------------------------------------------------------------
# Projetos
# --------------------------------------------------------------------------
class TestProjetoAPI:
    def test_listar_projetos(self, api_client, projeto):
        resp = api_client.get(PROJETOS_URL)
        assert resp.status_code == 200
        assert len(resp.json()) == 1
        assert resp.json()[0]["nome"] == "Projeto Alpha"

    def test_listar_sem_projetos_retorna_lista_vazia(self, api_client):
        resp = api_client.get(PROJETOS_URL)
        assert resp.status_code == 200
        assert resp.json() == []

    def test_campos_retornados(self, api_client, projeto):
        resp = api_client.get(projeto_url(projeto.pk))
        assert resp.status_code == 200
        assert set(resp.json()) == {
            "id", "usuario", "nome", "descricao", "data_criacao", "data_atualizacao",
        }

    def test_criar_projeto(self, api_client, usuario):
        payload = {"usuario": usuario.pk, "nome": "Novo", "descricao": "x"}
        resp = api_client.post(PROJETOS_URL, payload, format="json")
        assert resp.status_code == 201
        assert Projeto.objects.filter(nome="Novo", usuario=usuario).exists()

    def test_criar_projeto_sem_nome_retorna_400(self, api_client, usuario):
        resp = api_client.post(PROJETOS_URL, {"usuario": usuario.pk}, format="json")
        assert resp.status_code == 400
        assert "nome" in resp.json()

    def test_criar_projeto_sem_usuario_retorna_400(self, api_client):
        resp = api_client.post(PROJETOS_URL, {"nome": "X"}, format="json")
        assert resp.status_code == 400
        assert "usuario" in resp.json()

    def test_criar_projeto_usuario_inexistente_retorna_400(self, api_client):
        resp = api_client.post(PROJETOS_URL, {"usuario": 9999, "nome": "X"}, format="json")
        assert resp.status_code == 400

    def test_nome_acima_de_200_caracteres_retorna_400(self, api_client, usuario):
        payload = {"usuario": usuario.pk, "nome": "a" * 201}
        resp = api_client.post(PROJETOS_URL, payload, format="json")
        assert resp.status_code == 400

    def test_datas_sao_somente_leitura(self, api_client, usuario):
        payload = {"usuario": usuario.pk, "nome": "Datas", "data_criacao": "2000-01-01T00:00:00Z"}
        resp = api_client.post(PROJETOS_URL, payload, format="json")
        assert resp.status_code == 201
        assert not resp.json()["data_criacao"].startswith("2000")

    def test_detalhar_inexistente_retorna_404(self, api_client):
        assert api_client.get(projeto_url(9999)).status_code == 404

    def test_atualizar_projeto_put(self, api_client, projeto, usuario):
        payload = {"usuario": usuario.pk, "nome": "Renomeado", "descricao": ""}
        resp = api_client.put(projeto_url(projeto.pk), payload, format="json")
        assert resp.status_code == 200
        projeto.refresh_from_db()
        assert projeto.nome == "Renomeado"

    def test_atualizar_projeto_patch(self, api_client, projeto):
        resp = api_client.patch(projeto_url(projeto.pk), {"descricao": "nova"}, format="json")
        assert resp.status_code == 200
        projeto.refresh_from_db()
        assert projeto.descricao == "nova"

    def test_excluir_projeto_remove_tarefas(self, api_client, projeto, tarefa):
        resp = api_client.delete(projeto_url(projeto.pk))
        assert resp.status_code == 204
        assert not Tarefa.objects.filter(pk=tarefa.pk).exists()


# --------------------------------------------------------------------------
# Tarefas
# --------------------------------------------------------------------------
class TestTarefaAPI:
    def test_listar_tarefas(self, api_client, tarefa):
        resp = api_client.get(TAREFAS_URL)
        assert resp.status_code == 200
        assert [t["titulo"] for t in resp.json()] == ["Primeira tarefa"]

    def test_campos_retornados(self, api_client, tarefa):
        resp = api_client.get(tarefa_url(tarefa.pk))
        assert resp.status_code == 200
        assert set(resp.json()) == {
            "id", "projeto", "titulo", "descricao", "status", "prioridade",
            "prazo", "data_criacao", "data_atualizacao",
        }

    def test_criar_tarefa_aplica_defaults(self, api_client, projeto):
        resp = api_client.post(TAREFAS_URL, {"projeto": projeto.pk, "titulo": "Nova"}, format="json")
        assert resp.status_code == 201
        body = resp.json()
        assert body["status"] == "PENDENTE"
        assert body["prioridade"] == "MEDIA"
        assert body["prazo"] is None

    def test_criar_tarefa_completa(self, api_client, projeto):
        payload = {
            "projeto": projeto.pk, "titulo": "Completa", "descricao": "d",
            "status": "EM_ANDAMENTO", "prioridade": "ALTA", "prazo": "2030-12-31",
        }
        resp = api_client.post(TAREFAS_URL, payload, format="json")
        assert resp.status_code == 201
        assert resp.json()["prazo"] == "2030-12-31"

    @pytest.mark.parametrize("campo,valor", [
        ("status", "INVALIDO"),
        ("prioridade", "URGENTE"),
        ("prazo", "31/12/2030"),
    ])
    def test_valores_invalidos_retornam_400(self, api_client, projeto, campo, valor):
        payload = {"projeto": projeto.pk, "titulo": "Válida", campo: valor}
        resp = api_client.post(TAREFAS_URL, payload, format="json")
        assert resp.status_code == 400
        assert campo in resp.json()

    def test_criar_sem_titulo_retorna_400(self, api_client, projeto):
        resp = api_client.post(TAREFAS_URL, {"projeto": projeto.pk}, format="json")
        assert resp.status_code == 400
        assert "titulo" in resp.json()

    def test_criar_sem_projeto_retorna_400(self, api_client):
        resp = api_client.post(TAREFAS_URL, {"titulo": "Órfã"}, format="json")
        assert resp.status_code == 400
        assert "projeto" in resp.json()

    def test_criar_com_projeto_inexistente_retorna_400(self, api_client):
        resp = api_client.post(TAREFAS_URL, {"projeto": 9999, "titulo": "X Y"}, format="json")
        assert resp.status_code == 400

    @pytest.mark.xfail(
        strict=True,
        reason="BUG: título < 3 caracteres gera AttributeError (HTTP 500) em vez de 400. "
        "Ver docs/testes-api-tasks.md.",
    )
    def test_titulo_curto_retorna_400(self, api_client, projeto):
        api_client.raise_request_exception = False
        resp = api_client.post(TAREFAS_URL, {"projeto": projeto.pk, "titulo": "ab"}, format="json")
        assert resp.status_code == 400

    def test_atualizar_status_patch(self, api_client, tarefa):
        resp = api_client.patch(tarefa_url(tarefa.pk), {"status": "CONCLUIDA"}, format="json")
        assert resp.status_code == 200
        tarefa.refresh_from_db()
        assert tarefa.status == "CONCLUIDA"

    def test_atualizar_tarefa_put(self, api_client, tarefa, projeto):
        payload = {"projeto": projeto.pk, "titulo": "Editada", "prioridade": "BAIXA"}
        resp = api_client.put(tarefa_url(tarefa.pk), payload, format="json")
        assert resp.status_code == 200
        tarefa.refresh_from_db()
        assert (tarefa.titulo, tarefa.prioridade) == ("Editada", "BAIXA")

    def test_excluir_tarefa(self, api_client, tarefa):
        assert api_client.delete(tarefa_url(tarefa.pk)).status_code == 204
        assert not Tarefa.objects.filter(pk=tarefa.pk).exists()

    def test_detalhar_inexistente_retorna_404(self, api_client):
        assert api_client.get(tarefa_url(9999)).status_code == 404


# --------------------------------------------------------------------------
# Comportamento atual de acesso (documenta o estado, não o desejado)
# --------------------------------------------------------------------------
class TestAcessoAtual:
    """Registra que hoje a API NÃO exige autenticação nem filtra por dono.

    Quando autenticação/ownership forem implementados, estes testes devem
    ser substituídos por testes que esperem 401/403/404.
    """

    def test_anonimo_consegue_listar_projetos(self, api_client, projeto):
        assert api_client.get(PROJETOS_URL).status_code == 200

    def test_usuario_ve_projetos_de_outros(self, api_client, outro_usuario, projeto):
        api_client.force_authenticate(outro_usuario)
        resp = api_client.get(PROJETOS_URL)
        assert [p["id"] for p in resp.json()] == [projeto.pk]

    def test_usuario_pode_criar_projeto_em_nome_de_outro(self, api_client, usuario, outro_usuario):
        api_client.force_authenticate(usuario)
        payload = {"usuario": outro_usuario.pk, "nome": "Spoof"}
        resp = api_client.post(PROJETOS_URL, payload, format="json")
        assert resp.status_code == 201
        assert resp.json()["usuario"] == outro_usuario.pk
