# AGENTS.md — Contexto do repositório para agentes de IA

Leia antes de qualquer tarefa. Descreve **o que existe** no projeto. Confira sempre com o código.

## Contexto
- Trabalho da Unidade 02 de **Manutenção de Software** (UFERSA), com o enunciado em
  `Trabalho_Uni02_-_Manuteno.pdf` (não versionado).
- Uma API REST de **gerenciamento de tarefas**, feita sobre o projeto base *Django Quick Project*
  (lisa-ufersa/django-quickproject).
- **Regra da equipe:** seguir o padrão que já existe no repositório. Não adicionar tecnologia,
  funcionalidade ou assunto novo sem pedido explícito. Manter o escopo no que a atividade pede.

## Stack
Python 3.10+ · Django 4.2.3 · Django REST Framework 3.14 · drf-spectacular (Swagger) · SQLite ·
pytest + pytest-django. O `drf-yasg` está no `requirements.txt`, mas não é usado.

## Estrutura
| Caminho | Conteúdo |
|---|---|
| `config/` | `settings.py` (apps, DRF com auth Basic/Session/Token, spectacular) e `urls.py` (SimpleRouter, rotas na raiz) |
| `tasks/models.py` | `StatusTarefa`, `Prioridade`, `Projeto` (FK `usuario` → `User`), `Tarefa` (FK `projeto`) e as constantes `TITULO_TAMANHO_MINIMO` e `MENSAGEM_TITULO_CURTO` |
| `tasks/api/serializers.py` | `ProjetoSerializer`, `TarefaSerializer` (com `validate_titulo`) |
| `tasks/api/views.py` | `ProjetoViewSet`, `TarefaViewSet` (ModelViewSet) |
| `tasks/migrations/` | `0001_initial` |
| `tasks/tests.py` | `TarefaAPITestCase` (APITestCase), com 8 testes |
| `users/` | Exemplo do projeto base: `UserProfileExample`, ViewSet com `AllowAny` (GET/PUT), teste de exemplo |
| `docs/diagrama.iuml` | Diagrama de classes (PlantUML) |
| `docs/testes-api-tasks.md` | Documentação detalhada dos testes |

**Padrões:** cada app tem seu subpacote `api/` (views + serializers), os nomes de domínio são em
português e os testes ficam em `tests.py` dentro do app, no estilo `APITestCase`.

## Endpoints
| Rota | Operações |
|---|---|
| `/projetos/`, `/projetos/{id}/` | CRUD completo |
| `/tarefas/`, `/tarefas/{id}/` | CRUD completo |
| `/users/`, `/users/{id}/` | GET, PUT |
| `/api/token-auth/` | POST (gera token) |
| `/schema/`, `/swagger/`, `/admin/` | OpenAPI, Swagger UI, Django Admin |

As views não têm `permission_classes`, então a API é aberta (padrão `AllowAny`).

## Regras de negócio
| Regra | Estado |
|---|---|
| RN01: título ≥ 3 caracteres | ✅ Implementada e testada (`400`) |
| RN02: prazo não pode ser anterior à criação | ❌ Não implementada |
| RN03: status padrão `PENDENTE` | ✅ Implementada e testada |
| RN04: usuário sem dois projetos ativos com o mesmo nome | ❌ Não implementada (não existe campo "ativo") |
| RN05: não excluir projeto com tarefas `PENDENTE` ou `EM_ANDAMENTO` | ❌ Não implementada (hoje é `CASCADE`, e o teste `test_excluir_projeto_remove_tarefas` reflete isso) |
| RN06: prioridade `ALTA` exige prazo | ❌ Não implementada |

## Comandos
```bash
. venv/bin/activate && pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py test -v 2     # ou: pytest
```

## Pontos de atenção
- `db.sqlite3` está versionado no git e não tem as tabelas de `tasks` até rodar `migrate`.
- `SECRET_KEY` fica fixa em `settings.py`, com `DEBUG=True`. Nunca exponha os valores.
- O README ainda é o tutorial genérico do projeto base (a Etapa 1 pede um README atualizado).
- Branches: `main`, `develop`, `teste` (testes e correções, ainda sem merge).
