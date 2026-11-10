# Testes Unitários — API de Tarefas

Documentação dos testes automatizados da API do app `tasks` (Etapa 3 do trabalho).

- **Arquivo dos testes:** [`tasks/tests.py`](../tasks/tests.py)
- **Ferramenta:** `rest_framework.test.APITestCase`, do Django REST Framework
- **Padrão seguido:** o mesmo do projeto base (`users/tests.py`), com um arquivo `tests.py` dentro do app

---

## 1. Como executar

### 1.1 Preparar o ambiente (apenas na primeira vez)

```bash
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
```

### 1.2 Rodar os testes

| Objetivo | Comando |
|---|---|
| Rodar todos os testes do projeto | `python manage.py test` |
| Rodar com o nome de cada teste (detalhado) | `python manage.py test -v 2` |
| Rodar apenas o app `tasks` | `python manage.py test tasks` |
| Rodar um único teste | `python manage.py test tasks.tests.TarefaAPITestCase.test_cadastrar_tarefa` |
| Alternativa com pytest (configurado em `pytest.ini`) | `pytest -v` |

### 1.3 O que acontece durante a execução

1. O Django cria um **banco de dados de teste temporário** (em memória). O `db.sqlite3` **não** é alterado.
2. Antes de **cada** teste, o método `setUp` monta os dados iniciais.
3. O teste faz uma requisição HTTP à API pelo `self.client` (um `APIClient` do DRF) e confere a resposta e o banco com `assert...`.
4. Ao fim de cada teste, os dados são descartados, para que um teste não interfira no outro.
5. No final, o banco temporário é destruído.

---

## 2. Dados iniciais (`setUp`)

Antes de cada teste, são criados:

| Objeto | Valores |
|---|---|
| `self.usuario` | `User` com `username="usuario_teste"` |
| `self.projeto` | `Projeto` com `nome="Projeto Teste"`, pertencente a `self.usuario` |
| `self.tarefa` | `Tarefa` com `titulo="Tarefa existente"` no `self.projeto` (status `PENDENTE` e prioridade `MEDIA`, que são os valores padrão) |

Ou seja, todo teste começa com **1 projeto** e **1 tarefa** no banco.

> Nos exemplos abaixo, os `id` aparecem como `1`. Na execução real eles podem variar, e os
> testes usam sempre `self.projeto.id` e `self.tarefa.id`. As datas são preenchidas
> automaticamente com o horário da execução.

---

## 3. Detalhamento de cada teste

### 3.1 `test_cadastrar_tarefa` — Cadastro

**Objetivo:** verificar que a API cria uma tarefa nova.

**Entrada**
```http
POST /tarefas/
Content-Type: application/json

{"projeto": 1, "titulo": "Nova tarefa", "prazo": "2030-12-31"}
```

**Saída obtida**
```http
HTTP 201 Created

{
  "id": 2,
  "projeto": 1,
  "titulo": "Nova tarefa",
  "descricao": "",
  "status": "PENDENTE",
  "prioridade": "MEDIA",
  "prazo": "2030-12-31",
  "data_criacao": "2026-11-07T17:38:14.314186Z",
  "data_atualizacao": "2026-11-07T17:38:14.314199Z"
}
```

**Verificações**
- Status HTTP é `201 Created`
- O banco passa de 1 para **2** tarefas
- O `titulo` da resposta é `"Nova tarefa"`

---

### 3.2 `test_consultar_tarefas` — Consulta

**Objetivo:** verificar a listagem e a busca de uma tarefa pelo `id`.

**Entrada 1: listagem**
```http
GET /tarefas/
```
**Saída obtida**
```http
HTTP 200 OK

[
  {
    "id": 1,
    "projeto": 1,
    "titulo": "Tarefa existente",
    "descricao": "",
    "status": "PENDENTE",
    "prioridade": "MEDIA",
    "prazo": null,
    "data_criacao": "2026-11-07T17:38:14.435438Z",
    "data_atualizacao": "2026-11-07T17:38:14.435448Z"
  }
]
```

**Entrada 2: detalhe**
```http
GET /tarefas/1/
```
**Saída obtida**
```http
HTTP 200 OK

{"id": 1, "projeto": 1, "titulo": "Tarefa existente", "status": "PENDENTE", "prioridade": "MEDIA", "prazo": null, ...}
```

**Verificações**
- As duas requisições retornam `200 OK`
- A lista contém **1** tarefa
- O detalhe retorna `titulo` igual a `"Tarefa existente"`

---

### 3.3 `test_atualizar_tarefa` — Atualização

**Objetivo:** verificar a atualização parcial de uma tarefa (mudança de status).

**Entrada**
```http
PATCH /tarefas/1/
Content-Type: application/json

{"status": "CONCLUIDA"}
```

**Saída obtida**
```http
HTTP 200 OK

{
  "id": 1,
  "projeto": 1,
  "titulo": "Tarefa existente",
  "descricao": "",
  "status": "CONCLUIDA",
  "prioridade": "MEDIA",
  "prazo": null,
  "data_criacao": "2026-11-07T17:38:14.557930Z",
  "data_atualizacao": "2026-11-07T17:38:14.559667Z"
}
```

**Verificações**
- Status HTTP é `200 OK`
- Depois de recarregar do banco (`refresh_from_db`), o `status` da tarefa é `CONCLUIDA`
- Também dá para ver na saída que `data_atualizacao` mudou automaticamente

---

### 3.4 `test_excluir_tarefa` — Exclusão

**Objetivo:** verificar que a API remove uma tarefa.

**Entrada**
```http
DELETE /tarefas/1/
```

**Saída obtida**
```http
HTTP 204 No Content
(sem corpo)
```

**Verificações**
- Status HTTP é `204 No Content`
- A tarefa com esse `id` **não existe mais** no banco

---

### 3.5 `test_status_padrao_pendente` — Regra de negócio

**Objetivo:** garantir a regra "uma tarefa criada sem status começa como `PENDENTE`"
(`default=StatusTarefa.PENDENTE` em `tasks/models.py`).

**Entrada** (sem o campo `status`)
```http
POST /tarefas/
Content-Type: application/json

{"projeto": 1, "titulo": "Sem status"}
```

**Saída obtida**
```http
HTTP 201 Created

{
  "id": 2,
  "projeto": 1,
  "titulo": "Sem status",
  "descricao": "",
  "status": "PENDENTE",
  "prioridade": "MEDIA",
  "prazo": null,
  ...
}
```

**Verificações**
- Status HTTP é `201 Created`
- O `status` da resposta é `"PENDENTE"`

---

### 3.6 `test_status_invalido` — Validação

**Objetivo:** garantir que só são aceitos os status `PENDENTE`, `EM_ANDAMENTO` e `CONCLUIDA`.

**Entrada**
```http
POST /tarefas/
Content-Type: application/json

{"projeto": 1, "titulo": "Status errado", "status": "INVALIDO"}
```

**Saída obtida**
```http
HTTP 400 Bad Request

{"status": ["\"INVALIDO\" is not a valid choice."]}
```

**Verificações**
- Status HTTP é `400 Bad Request`
- A resposta indica o erro no campo `status`

---

### 3.7 `test_titulo_curto_invalido` — Regra de negócio

**Objetivo:** garantir a regra "o título da tarefa deve ter no mínimo 3 caracteres"
(`validate_titulo` em `tasks/api/serializers.py` e `clean()` em `tasks/models.py`).

**Entrada** (título com 2 caracteres)
```http
POST /tarefas/
Content-Type: application/json

{"projeto": 1, "titulo": "ab"}
```

**Saída obtida**
```http
HTTP 400 Bad Request

{"titulo": ["O título da tarefa deve ter, no mínimo, 3 caracteres."]}
```

**Verificações**
- Status HTTP é `400 Bad Request`
- A resposta indica o erro no campo `titulo`
- O banco continua com apenas **1** tarefa, ou seja, nada foi gravado

---

### 3.8 `test_excluir_projeto_remove_tarefas` — Regra de negócio / relacionamento

**Objetivo:** verificar o relacionamento Projeto → Tarefa. Ao excluir um projeto, suas tarefas
também são excluídas (`on_delete=models.CASCADE` em `Tarefa.projeto`).

**Entrada**
```http
DELETE /projetos/1/
```

**Saída obtida**
```http
HTTP 204 No Content
(sem corpo)
```

**Verificações**
- Status HTTP é `204 No Content`
- O banco fica com **0** tarefas (a tarefa do projeto foi removida junto)

---

## 4. Resumo: requisitos da Etapa 3 × testes

| Requisito do trabalho | Teste(s) |
|---|---|
| Pelo menos 4 testes automatizados com Django/DRF | 8 testes com `APITestCase` |
| Operação de cadastro | `test_cadastrar_tarefa` |
| Operação de consulta | `test_consultar_tarefas` |
| Operação de atualização ou exclusão | `test_atualizar_tarefa`, `test_excluir_tarefa` |
| Validação ou regra de negócio | `test_status_padrao_pendente`, `test_status_invalido`, `test_titulo_curto_invalido`, `test_excluir_projeto_remove_tarefas` |
| Executar e apresentar os resultados | Seção 5 |

---

## 4.1 Regras de negócio × testes

| Regra | Descrição | Implementada | Testada | Teste |
|---|---|---|---|---|
| RN01 | O título da tarefa deve ter, no mínimo, 3 caracteres | ✅ `Tarefa.clean()` + `TarefaSerializer.validate_titulo` | ✅ | `test_titulo_curto_invalido` |
| RN02 | A data de prazo não pode ser anterior à data de criação | ❌ | ❌ | — |
| RN03 | Sem status enviado, a tarefa assume `PENDENTE` | ✅ `default=StatusTarefa.PENDENTE` | ✅ | `test_status_padrao_pendente` |
| RN04 | Um usuário não pode ter dois projetos ativos com o mesmo nome | ❌ | ❌ | — |
| RN05 | Projeto com tarefas `PENDENTE` ou `EM_ANDAMENTO` não pode ser excluído | ❌ | ❌ | — |
| RN06 | Tarefa com prioridade `ALTA` precisa ter prazo | ❌ | ❌ | — |

> As regras RN02, RN04, RN05 e RN06 ainda não estão no código, por isso não têm teste.
> Atenção: `test_excluir_projeto_remove_tarefas` exclui um projeto que tem uma tarefa `PENDENTE`.
> Se a RN05 for implementada, esse teste deve passar a esperar a exclusão **bloqueada**.

## 4.2 Validações × testes

| Validação | Onde | Testada | Teste |
|---|---|---|---|
| `status` só aceita `PENDENTE`, `EM_ANDAMENTO` ou `CONCLUIDA` | `choices` em `Tarefa.status` | ✅ | `test_status_invalido` |
| `titulo` com no mínimo 3 caracteres (RN01) | `validate_titulo` no serializer | ✅ | `test_titulo_curto_invalido` |
| Relacionamento Projeto → Tarefa com exclusão em cascata | `on_delete=CASCADE` | ✅ | `test_excluir_projeto_remove_tarefas` |
| `prioridade` só aceita `BAIXA`, `MEDIA` ou `ALTA` | `choices` em `Tarefa.prioridade` | ❌ | — |
| Campos obrigatórios (`titulo`, `projeto`, `nome`, `usuario`) | Serializers (`ModelSerializer`) | ❌ | — |

---

## 5. Resultado da execução

```
$ python manage.py test -v 2
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Found 9 test(s).
...
System check identified no issues (0 silenced).
test_atualizar_tarefa (tasks.tests.TarefaAPITestCase.test_atualizar_tarefa) ... ok
test_cadastrar_tarefa (tasks.tests.TarefaAPITestCase.test_cadastrar_tarefa) ... ok
test_consultar_tarefas (tasks.tests.TarefaAPITestCase.test_consultar_tarefas) ... ok
test_excluir_projeto_remove_tarefas (tasks.tests.TarefaAPITestCase.test_excluir_projeto_remove_tarefas) ... ok
test_excluir_tarefa (tasks.tests.TarefaAPITestCase.test_excluir_tarefa) ... ok
test_status_invalido (tasks.tests.TarefaAPITestCase.test_status_invalido) ... ok
test_status_padrao_pendente (tasks.tests.TarefaAPITestCase.test_status_padrao_pendente) ... ok
test_titulo_curto_invalido (tasks.tests.TarefaAPITestCase.test_titulo_curto_invalido) ... ok
test_user (users.tests.UserTestCase.test_user)
test example ... ok

----------------------------------------------------------------------
Ran 9 tests in 0.984s

OK
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
```

**Resultado: 9 testes executados, 9 aprovados (`OK`)**. São 8 testes do app `tasks` e 1 teste de
exemplo do app `users`, que já vinha no projeto base.

### Como ler o resultado

| Saída | Significado |
|---|---|
| `... ok` | O teste passou |
| `... FAIL` | Uma verificação (`assert...`) não foi atendida |
| `... ERROR` | Aconteceu uma exceção inesperada durante o teste |
| `OK` no final | Todos os testes passaram |
| `FAILED (failures=N, errors=M)` no final | Algum teste falhou |

---

