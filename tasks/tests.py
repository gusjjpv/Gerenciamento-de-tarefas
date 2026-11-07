from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from tasks.models import Projeto, StatusTarefa, Tarefa

# Create your tests here.


class TarefaAPITestCase(APITestCase):
    """ Testes da API de tarefas (/tarefas/) """

    def setUp(self) -> None:
        self.usuario = User.objects.create_user(username="usuario_teste", password="senha_teste")
        self.projeto = Projeto.objects.create(usuario=self.usuario, nome="Projeto Teste")
        self.tarefa = Tarefa.objects.create(projeto=self.projeto, titulo="Tarefa existente")

    def test_cadastrar_tarefa(self):
        """ Cadastro: POST /tarefas/ cria uma nova tarefa """
        dados = {"projeto": self.projeto.id, "titulo": "Nova tarefa", "prazo": "2030-12-31"}

        resposta = self.client.post("/tarefas/", dados, format="json")

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tarefa.objects.count(), 2)
        self.assertEqual(resposta.data["titulo"], "Nova tarefa")

    def test_consultar_tarefas(self):
        """ Consulta: GET /tarefas/ e GET /tarefas/{id}/ """
        resposta_lista = self.client.get("/tarefas/")
        resposta_detalhe = self.client.get(f"/tarefas/{self.tarefa.id}/")

        self.assertEqual(resposta_lista.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resposta_lista.data), 1)
        self.assertEqual(resposta_detalhe.status_code, status.HTTP_200_OK)
        self.assertEqual(resposta_detalhe.data["titulo"], "Tarefa existente")

    def test_atualizar_tarefa(self):
        """ Atualização: PATCH /tarefas/{id}/ altera o status """
        resposta = self.client.patch(
            f"/tarefas/{self.tarefa.id}/", {"status": StatusTarefa.CONCLUIDA}, format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_200_OK)
        self.tarefa.refresh_from_db()
        self.assertEqual(self.tarefa.status, StatusTarefa.CONCLUIDA)

    def test_excluir_tarefa(self):
        """ Exclusão: DELETE /tarefas/{id}/ remove a tarefa """
        resposta = self.client.delete(f"/tarefas/{self.tarefa.id}/")

        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Tarefa.objects.filter(id=self.tarefa.id).exists())

    def test_status_padrao_pendente(self):
        """ Regra de negócio: Ao ser criada, se nenhum status for explicitamente enviado,
        a tarefa deve assumir o estado padrão de PENDENTE """
        resposta = self.client.post(
            "/tarefas/", {"projeto": self.projeto.id, "titulo": "Sem status"}, format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resposta.data["status"], StatusTarefa.PENDENTE)

    def test_status_invalido(self):
        """ Validação: status fora das opções é rejeitado com 400 """
        resposta = self.client.post(
            "/tarefas/",
            {"projeto": self.projeto.id, "titulo": "Status errado", "status": "INVALIDO"},
            format="json",
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("status", resposta.data)

    def test_titulo_curto_invalido(self):
        """ Regra de negócio: O título da tarefa deve ter, no mínimo, 3 caracteres. """
        resposta = self.client.post(
            "/tarefas/", {"projeto": self.projeto.id, "titulo": "ab"}, format="json"
        )

        self.assertEqual(resposta.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("titulo", resposta.data)
        self.assertEqual(Tarefa.objects.count(), 1)

    def test_excluir_projeto_remove_tarefas(self):
        """ Relacionamento: excluir o projeto exclui suas tarefas (CASCADE) """
        resposta = self.client.delete(f"/projetos/{self.projeto.id}/")

        self.assertEqual(resposta.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tarefa.objects.count(), 0)
