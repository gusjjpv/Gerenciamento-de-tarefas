# Testes Unitários — API de Tarefas

Testes automatizados da API do app `tasks`, criados com os recursos do **Django REST Framework**
(`rest_framework.test.APITestCase`). Seguem o mesmo padrão do projeto base (`users/tests.py`):
um arquivo `tests.py` dentro do app.

Arquivo: [`tasks/tests.py`](../tasks/tests.py)

## Como executar

```bash
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate     # cria as tabelas de projetos e tarefas
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
| `test_titulo_curto_invalido` | Regra de negócio | Título com menos de 3 caracteres retorna `400` e não grava a tarefa |
| `test_excluir_projeto_remove_tarefas` | Regra de negócio / relacionamento | Excluir um projeto exclui suas tarefas (`on_delete=CASCADE`) |

## Resultado da execução

```
$ python manage.py test -v 2
Atualização: PATCH /tarefas/{id}/ altera o status ... ok
Cadastro: POST /tarefas/ cria uma nova tarefa ... ok
Consulta: GET /tarefas/ e GET /tarefas/{id}/ ... ok
Regra de negócio: excluir o projeto exclui suas tarefas (relacionamento) ... ok
Exclusão: DELETE /tarefas/{id}/ remove a tarefa ... ok
Validação: status fora das opções é rejeitado com 400 ... ok
Regra de negócio: tarefa criada sem status recebe PENDENTE ... ok
Regra de negócio: título com menos de 3 caracteres é rejeitado com 400 ... ok
test example ... ok

----------------------------------------------------------------------
Ran 9 tests

OK
```

(8 testes do app `tasks` + 1 teste de exemplo do app `users`, que já existia no projeto base.)

## Correções feitas durante os testes

Os testes ajudaram a encontrar dois problemas, que foram corrigidos:

| Problema | Causa | Correção |
|---|---|---|
| Título com menos de 3 caracteres retornava erro `500` | `tasks/models.py` usava `models.ValidationError`, que não existe em `django.db.models`. Além disso, o DRF não converte o `ValidationError` do model em resposta `400`. | `tasks/models.py` passou a importar `ValidationError` de `django.core.exceptions`. O `TarefaSerializer` (`tasks/api/serializers.py`) ganhou o método `validate_titulo`, que devolve `400`. O limite e a mensagem ficaram em constantes (`TITULO_TAMANHO_MINIMO`, `MENSAGEM_TITULO_CURTO`) usadas pelo model e pelo serializer, sem duplicação. |
| Tabelas de projetos e tarefas não existiam no banco | O app `tasks` não tinha migrations | Foi gerada a migration `tasks/migrations/0001_initial.py`. Para aplicá-la: `python manage.py migrate`. |
