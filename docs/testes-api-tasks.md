# Testes Unitários — API de Tarefas

Testes automatizados da API do app `tasks`, criados com os recursos do **Django REST Framework**
(`rest_framework.test.APITestCase`). Seguem o mesmo padrão do projeto base (`users/tests.py`):
um arquivo `tests.py` dentro do app.

Arquivo: [`tasks/tests.py`](../tasks/tests.py)

## Como executar

```bash
. venv/bin/activate
pip install -r requirements.txt
python manage.py test        # executor do Django
# ou
pytest                       # executor configurado em pytest.ini
```

Os testes rodam em um banco de dados temporário, então o `db.sqlite3` não é alterado.

## Testes implementados

Classe `TarefaAPITestCase`. O `setUp` cria um usuário, um projeto e uma tarefa.

| Teste | Requisito atendido | O que verifica |
|---|---|---|
| `test_cadastrar_tarefa` | Cadastro | `POST /tarefas/` retorna `201` e a tarefa é gravada |
| `test_consultar_tarefas` | Consulta | `GET /tarefas/` e `GET /tarefas/{id}/` retornam `200` com os dados |
| `test_atualizar_tarefa` | Atualização | `PATCH /tarefas/{id}/` altera o status para `CONCLUIDA` |
| `test_excluir_tarefa` | Exclusão | `DELETE /tarefas/{id}/` retorna `204` e remove a tarefa |
| `test_status_padrao_pendente` | Regra de negócio | Tarefa criada sem status recebe `PENDENTE` |
| `test_status_invalido` | Validação | Status fora das opções (`PENDENTE`, `EM_ANDAMENTO`, `CONCLUIDA`) retorna `400` |
| `test_excluir_projeto_remove_tarefas` | Regra de negócio / relacionamento | Excluir um projeto exclui suas tarefas (`on_delete=CASCADE`) |

## Resultado da execução

```
$ python manage.py test -v 2
test_atualizar_tarefa (tasks.tests.TarefaAPITestCase.test_atualizar_tarefa) ... ok
test_cadastrar_tarefa (tasks.tests.TarefaAPITestCase.test_cadastrar_tarefa) ... ok
test_consultar_tarefas (tasks.tests.TarefaAPITestCase.test_consultar_tarefas) ... ok
test_excluir_projeto_remove_tarefas (tasks.tests.TarefaAPITestCase.test_excluir_projeto_remove_tarefas) ... ok
test_excluir_tarefa (tasks.tests.TarefaAPITestCase.test_excluir_tarefa) ... ok
test_status_invalido (tasks.tests.TarefaAPITestCase.test_status_invalido) ... ok
test_status_padrao_pendente (tasks.tests.TarefaAPITestCase.test_status_padrao_pendente) ... ok
test_user (users.tests.UserTestCase.test_user) ... ok

Ran 8 tests

OK
```

## Observação

A regra "título com no mínimo 3 caracteres" (`Tarefa.clean()` em `tasks/models.py`) ainda não
tem teste. O código usa `models.ValidationError`, que não existe em `django.db.models`, e por
isso um título curto gera erro `500` em vez de `400`. Depois que esse ponto for corrigido, o
teste correspondente pode ser adicionado.
