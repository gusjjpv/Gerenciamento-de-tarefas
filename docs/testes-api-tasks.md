# Testes da API de Tarefas (`tasks`)

Documentação dos testes unitários e de API do app `tasks` (Projetos e Tarefas).

## Como executar

```bash
. venv/bin/activate
pip install -r requirements.txt
pytest                      # todos os testes do projeto
pytest tasks -v             # apenas o app tasks
pytest tasks/tests/test_api.py::TestTarefaAPI -v   # uma classe específica
```

A configuração está em [`pytest.ini`](../pytest.ini) (`DJANGO_SETTINGS_MODULE = config.settings`).
O pytest-django cria um **banco de testes temporário**, então o `db.sqlite3` não é tocado.

> **Nota:** o app `tasks` ainda não tem a pasta `migrations/`. Os testes funcionam assim mesmo,
> porque o Django cria as tabelas de apps sem migrations ao montar o banco de testes. Já em
> execução normal (`runserver`), é preciso rodar `python manage.py makemigrations tasks && python manage.py migrate`.

**Resultado atual:** `44 passed, 2 xfailed`

## Estrutura

```
tasks/tests/
├── __init__.py
├── conftest.py      # fixtures compartilhadas
├── test_models.py   # regras dos models Projeto e Tarefa
└── test_api.py      # endpoints /projetos/ e /tarefas/
```

### Fixtures (`conftest.py`)

| Fixture | O que fornece |
|---|---|
| `api_client` | `rest_framework.test.APIClient` sem autenticação |
| `usuario` | `User` "dono" |
| `outro_usuario` | Segundo `User`, usado nos cenários de acesso |
| `projeto` | `Projeto` "Projeto Alpha" do `usuario` |
| `tarefa` | `Tarefa` "Primeira tarefa" no `projeto` |

## Endpoints cobertos

| Método | Rota | Descrição |
|---|---|---|
| GET | `/projetos/` | Lista projetos |
| POST | `/projetos/` | Cria projeto (`usuario`, `nome` obrigatórios) |
| GET/PUT/PATCH/DELETE | `/projetos/{id}/` | Detalha, atualiza e remove (a remoção apaga as tarefas em cascata) |
| GET | `/tarefas/` | Lista tarefas |
| POST | `/tarefas/` | Cria tarefa (`projeto`, `titulo` obrigatórios) |
| GET/PUT/PATCH/DELETE | `/tarefas/{id}/` | Detalha, atualiza e remove |

## Casos de teste

### `test_models.py`

**`TestProjeto`**
- `__str__` retorna o `nome`
- `data_criacao` e `data_atualizacao` são preenchidas automaticamente
- `descricao` é opcional (padrão `""`)
- `related_name` `usuario.projetos`
- Excluir o usuário remove seus projetos (CASCADE)

**`TestTarefa`**
- `__str__` retorna o `titulo`
- Status padrão `PENDENTE`, prioridade padrão `MEDIA`, `prazo` opcional
- `related_name` `projeto.tarefas`
- Excluir o projeto remove suas tarefas (CASCADE)
- Título com exatamente 3 caracteres é aceito
- Status fora dos choices é rejeitado pelo `full_clean()` chamado no `save()`
- ⚠️ `xfail`: título com menos de 3 caracteres deveria levantar `ValidationError` (ver bug B1)

### `test_api.py`

**`TestProjetoAPI`**
- Listagem (com e sem registros) e campos retornados
- Criação válida → `201`
- Sem `nome`, sem `usuario`, `usuario` inexistente ou `nome` com mais de 200 caracteres → `400`
- `data_criacao` é somente leitura (valor enviado é ignorado)
- Detalhe inexistente → `404`
- `PUT` e `PATCH` → `200`
- `DELETE` → `204` e remove as tarefas em cascata

**`TestTarefaAPI`**
- Listagem e campos retornados
- Criação mínima aplica os padrões (`PENDENTE`, `MEDIA`, `prazo=null`)
- Criação com todos os campos
- `status`, `prioridade` ou `prazo` inválidos → `400` (parametrizado)
- Sem `titulo`, sem `projeto` ou `projeto` inexistente → `400`
- `PATCH` de status, `PUT` completo, `DELETE` → `204`, detalhe inexistente → `404`
- ⚠️ `xfail`: título curto deveria retornar `400` (ver bug B1)

**`TestAcessoAtual`**: documenta o **comportamento atual**, não o desejado:
- Anônimo consegue listar projetos
- Usuário autenticado vê projetos de outros usuários
- Usuário consegue criar projeto em nome de outro (campo `usuario` gravável)

> Quando autenticação e controle de dono forem implementados, substituir esses testes por
> testes que esperem `401`, `403` ou `404`.

## Bugs conhecidos (testes `xfail`)

Os testes marcados com `@pytest.mark.xfail(strict=True)` passam a **falhar** assim que o bug for
corrigido. Isso serve de lembrete para remover o marcador.

| ID | Problema | Arquivo | Correção sugerida |
|---|---|---|---|
| B1 | `Tarefa.clean()` usa `models.ValidationError`, que não existe em `django.db.models`. Um título com menos de 3 caracteres gera `AttributeError`, e a API responde **500** em vez de **400**. | [`tasks/models.py`](../tasks/models.py) | Importar `from django.core.exceptions import ValidationError` **e** adicionar `validate_titulo` no `TarefaSerializer`, porque o DRF não converte o `ValidationError` do Django em 400. |

## Lacunas conhecidas (ainda sem teste por falta de regra definida)

- `validar_prazo()` aparece em [`diagrama.iuml`](diagrama.iuml), mas não está implementada nem especificada.
- Autenticação e permissões por dono ainda não foram implementadas (ver `TestAcessoAtual`).
