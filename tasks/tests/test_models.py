"""Testes unitários dos models do app tasks."""

import pytest

from tasks.models import Prioridade, Projeto, StatusTarefa, Tarefa

pytestmark = pytest.mark.django_db


class TestProjeto:
    def test_str_retorna_nome(self, projeto):
        assert str(projeto) == "Projeto Alpha"

    def test_datas_preenchidas_automaticamente(self, projeto):
        assert projeto.data_criacao is not None
        assert projeto.data_atualizacao is not None

    def test_descricao_opcional(self, usuario):
        p = Projeto.objects.create(usuario=usuario, nome="Sem descrição")
        assert p.descricao == ""

    def test_related_name_projetos(self, usuario, projeto):
        assert list(usuario.projetos.all()) == [projeto]

    def test_excluir_usuario_remove_projetos_em_cascata(self, usuario, projeto):
        usuario.delete()
        assert not Projeto.objects.filter(pk=projeto.pk).exists()


class TestTarefa:
    def test_str_retorna_titulo(self, tarefa):
        assert str(tarefa) == "Primeira tarefa"

    def test_status_padrao_pendente(self, tarefa):
        assert tarefa.status == StatusTarefa.PENDENTE

    def test_prioridade_padrao_media(self, tarefa):
        assert tarefa.prioridade == Prioridade.MEDIA

    def test_prazo_opcional(self, tarefa):
        assert tarefa.prazo is None

    def test_related_name_tarefas(self, projeto, tarefa):
        assert list(projeto.tarefas.all()) == [tarefa]

    def test_excluir_projeto_remove_tarefas_em_cascata(self, projeto, tarefa):
        projeto.delete()
        assert not Tarefa.objects.filter(pk=tarefa.pk).exists()

    def test_titulo_com_tres_caracteres_e_valido(self, projeto):
        t = Tarefa.objects.create(projeto=projeto, titulo="abc")
        assert t.pk is not None

    @pytest.mark.xfail(
        strict=True,
        raises=AttributeError,
        reason="BUG: tasks/models.py usa models.ValidationError (inexistente); "
        "deveria usar django.core.exceptions.ValidationError.",
    )
    def test_titulo_curto_levanta_validation_error(self, projeto):
        from django.core.exceptions import ValidationError

        with pytest.raises(ValidationError):
            Tarefa.objects.create(projeto=projeto, titulo="ab")

    def test_status_invalido_rejeitado_pelo_full_clean(self, projeto):
        from django.core.exceptions import ValidationError

        with pytest.raises(ValidationError):
            Tarefa.objects.create(projeto=projeto, titulo="Válida", status="INVALIDO")
