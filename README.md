# API de Gerenciamento de Tarefas (Task Management API)

API RESTful desenvolvida com **Django** e **Django Rest Framework (DRF)** para gerenciamento de projetos e tarefas, com persistência em banco de dados SQLite e documentação interativa via Swagger (drf-spectacular).

> Projeto desenvolvido para o Trabalho da Unidade 02 da disciplina de **Manutenção de Software** — Universidade Federal Rural do Semi-Árido (**UFERSA**).

---

## Sumário

- [Visão Geral](#visão-geral)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Modelagem de Dados e Arquitetura](#modelagem-de-dados-e-arquitetura)
- [Regras de Negócio e Validações](#regras-de-negócio-e-validações)
- [Instruções de Instalação e Execução](#instruções-de-instalação-e-execução)
- [Execução dos Testes Automatizados](#execução-dos-testes-automatizados)
- [Descrição dos Endpoints da API](#descrição-dos-endpoints-da-api)
  - [Documentação Interativa (Swagger / OpenAPI)](#documentação-interativa-swagger--openapi)
  - [Autenticação](#autenticação)
  - [Projetos (`/projetos/`)](#projetos-projetos)
  - [Tarefas (`/tarefas/`)](#tarefas-tarefas)
  - [Usuários (`/users/`)](#usuários-users)
  - [Django Admin (`/admin/`)](#django-admin-admin)
- [Exemplos Práticos de Uso](#exemplos-práticos-de-uso)
- [Estrutura do Repositório](#estrutura-do-repositório)

---

## Visão Geral

A **Task Management API** permite aos usuários organizar seus projetos e controlar tarefas associadas. Cada usuário pode criar e manter múltiplos projetos, e cada projeto pode conter um conjunto de tarefas com definições de prioridade, status de andamento e prazos limite.

---

## Tecnologias Utilizadas

- **Python** (3.10+)
- **Django** (4.2.3)
- **Django Rest Framework** (3.14.0)
- **drf-spectacular** (0.26.4) — Geração de documentação OpenAPI 3.0 e Swagger UI
- **SQLite** — Banco de dados relacional padrão
- **pytest** & **pytest-django** — Suíte de testes automatizados

---

## Modelagem de Dados e Arquitetura

O modelo de domínio é composto por duas entidades principais relacionadas entre si e integradas ao modelo de autenticação de usuários nativo do Django (`django.contrib.auth.models.User`).

O diagrama de classes completo em PlantUML pode ser consultado em [`docs/diagrama.iuml`](docs/diagrama.iuml).

### Entidades

#### 1. `Projeto`
Representa um projeto pertencente a um usuário.
- `id` (*IntegerField*, chave primária automática)
- `usuario` (*ForeignKey* para `User` com `on_delete=CASCADE`, `related_name="projetos"`)
- `nome` (*CharField*, tamanho máximo 200)
- `descricao` (*TextField*, opcional/em branco)
- `data_criacao` (*DateTimeField*, gerado automaticamente na criação)
- `data_atualizacao` (*DateTimeField*, atualizado automaticamente a cada modificação)

#### 2. `Tarefa`
Representa uma tarefa associada a um determinado projeto.
- `id` (*IntegerField*, chave primária automática)
- `projeto` (*ForeignKey* para `Projeto` com `on_delete=CASCADE`, `related_name="tarefas"`)
- `titulo` (*CharField*, tamanho máximo 200, mínimo de 3 caracteres)
- `descricao` (*TextField*, opcional/em branco)
- `status` (*CharField*, opções de `StatusTarefa`, padrão: `PENDENTE`)
- `prioridade` (*CharField*, opções de `Prioridade`, padrão: `MEDIA`)
- `prazo` (*DateField*, opcional/nulo)
- `data_criacao` (*DateTimeField*, gerado automaticamente na criação)
- `data_atualizacao` (*DateTimeField*, atualizado automaticamente a cada modificação)

### Enums

- **`StatusTarefa`**:
  - `PENDENTE` — Pendente (valor padrão)
  - `EM_ANDAMENTO` — Em andamento
  - `CONCLUIDA` — Concluída
- **`Prioridade`**:
  - `BAIXA` — Baixa
  - `MEDIA` — Média (valor padrão)
  - `ALTA` — Alta

---

## Regras de Negócio e Validações

1. **Validação de Tamanho Mínimo do Título da Tarefa (`RN01`)**:
   - O título da tarefa deve possuir, no mínimo, **3 caracteres**.
   - Caso uma requisição informe um título com menos de 3 caracteres, a requisição é rejeitada com mensagem de erro explicativa.
2. **Definição de Status Padrão (`RN03`)**:
   - Caso uma tarefa seja criada sem a especificação do campo `status`, o valor assumido automaticamente é `PENDENTE`.
3. **Definição de Prioridade Padrão**:
   - Caso uma tarefa seja criada sem a especificação do campo `prioridade`, o valor assumido automaticamente é `MEDIA`.
4. **Integridade Referencial e Exclusão em Cascata**:
   - Tarefas sempre estão vinculadas a um projeto existente.
   - A exclusão de um projeto remove automaticamente todas as tarefas associadas a ele (`CASCADE`).

---

## Instruções de Instalação e Execução

Siga os passos abaixo para configurar e executar a API em seu ambiente local:

### 1. Clonar o Repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd django-quickproject
```

### 2. Criar e Ativar o Ambiente Virtual

- **No Linux/macOS:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

- **No Windows:**
  ```bash
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Instalar as Dependências

```bash
pip install -r requirements.txt
```

### 4. Executar as Migrações do Banco de Dados

Gere e aplique as migrações para inicializar o esquema no SQLite:

```bash
python manage.py makemigrations tasks
python manage.py migrate
```

### 5. Criar Superusuário (Opcional)

Para acessar o painel do Django Admin e criar usuários:

```bash
python manage.py createsuperuser
```

> **Nota:** O banco de dados pré-configurado já inclui um usuário padrão:
> - **Usuário:** `admin`
> - **Senha:** `adminadmin`

### 6. Executar o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

O servidor estará ativo em: `http://127.0.0.1:8000/`.

---

## Execução dos Testes Automatizados

Para executar os testes com o **pytest**:

```bash
pytest
```

Ou através do gerenciador de testes padrão do Django:

```bash
python manage.py test -v 2
```

---

## Descrição dos Endpoints da API

### Documentação Interativa (Swagger / OpenAPI)

A API disponibiliza documentação interativa gerada automaticamente com **drf-spectacular**:

- **Swagger UI:** [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- **OpenAPI Schema (YAML/JSON):** [http://127.0.0.1:8000/schema/](http://127.0.0.1:8000/schema/)

---

### Autenticação

A API suporta autenticação via Token (`TokenAuthentication`), Basic Auth e Session Auth. Para obter um token via credenciais de usuário:

- **Rota:** `POST /api/token-auth/`
- **Corpo da Requisição:**
  ```json
  {
    "username": "admin",
    "password": "adminadmin"
  }
  ```
- **Resposta de Sucesso (`200 OK`):**
  ```json
  {
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
  }
  ```
- Para utilizar o token nas requisições subsequentes, envie o header HTTP:
  ```http
  Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
  ```

---

### Projetos (`/projetos/`)

Gerenciamento de projetos via `ModelViewSet` (operações CRUD completas):

| Método | Rota | Descrição | Status de Sucesso |
|---|---|---|---|
| `GET` | `/projetos/` | Lista todos os projetos cadastrados | `200 OK` |
| `POST` | `/projetos/` | Cria um novo projeto | `201 Created` |
| `GET` | `/projetos/{id}/` | Retorna os detalhes de um projeto específico | `200 OK` |
| `PUT` | `/projetos/{id}/` | Atualiza completamente um projeto existente | `200 OK` |
| `PATCH` | `/projetos/{id}/` | Atualiza parcialmente um projeto existente | `200 OK` |
| `DELETE` | `/projetos/{id}/` | Exclui um projeto e suas tarefas associadas | `204 No Content` |

#### Payload para Criação de Projeto (`POST /projetos/`)
```json
{
  "usuario": 1,
  "nome": "Sistema de Gestão Escolar",
  "descricao": "Desenvolvimento do módulo de matrículas e notas"
}
```

---

### Tarefas (`/tarefas/`)

Gerenciamento de tarefas vinculadas a projetos (operações CRUD completas):

| Método | Rota | Descrição | Status de Sucesso |
|---|---|---|---|
| `GET` | `/tarefas/` | Lista todas as tarefas | `200 OK` |
| `POST` | `/tarefas/` | Cria uma nova tarefa (com validação de título) | `201 Created` |
| `GET` | `/tarefas/{id}/` | Retorna os detalhes de uma tarefa específica | `200 OK` |
| `PUT` | `/tarefas/{id}/` | Atualiza completamente uma tarefa existente | `200 OK` |
| `PATCH` | `/tarefas/{id}/` | Atualiza parcialmente os campos de uma tarefa | `200 OK` |
| `DELETE` | `/tarefas/{id}/` | Exclui uma tarefa | `204 No Content` |

#### Payload para Criação de Tarefa (`POST /tarefas/`)
```json
{
  "projeto": 1,
  "titulo": "Implementar autenticação JWT",
  "descricao": "Adicionar suporte a tokens com expiração configurável",
  "status": "PENDENTE",
  "prioridade": "ALTA",
  "prazo": "2026-12-15"
}
```

> **Campos opcionais na criação:**
> - `descricao` (pode ser vazio)
> - `status` (assume `PENDENTE` caso omitido)
> - `prioridade` (assume `MEDIA` caso omitido)
> - `prazo` (pode ser nulo/omitido, formato aceito: `YYYY-MM-DD`)

---

### Usuários (`/users/`)

Exemplo de visualização de perfil de usuário do projeto base:

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/users/` | Lista perfis de usuário de exemplo |
| `GET` | `/users/{id}/` | Retorna detalhes do perfil especificado |
| `PUT` | `/users/{id}/` | Atualiza os dados do perfil |

---

### Django Admin (`/admin/`)

Interface administrativa para gerenciamento visual de tabelas, usuários e permissões:

- **URL:** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## Exemplos Práticos de Uso

### 1. Criar um Projeto com `curl`

```bash
curl -X POST http://127.0.0.1:8000/projetos/ \
  -H "Content-Type: application/json" \
  -d '{
    "usuario": 1,
    "nome": "Reformulação do Portal",
    "descricao": "Modernização do layout e infraestrutura"
  }'
```

**Resposta:**
```json
{
  "id": 1,
  "usuario": 1,
  "nome": "Reformulação do Portal",
  "descricao": "Modernização do layout e infraestrutura",
  "data_criacao": "2026-11-10T17:00:00Z",
  "data_atualizacao": "2026-11-10T17:00:00Z"
}
```

### 2. Criar uma Tarefa Válida

```bash
curl -X POST http://127.0.0.1:8000/tarefas/ \
  -H "Content-Type: application/json" \
  -d '{
    "projeto": 1,
    "titulo": "Criar tela de login",
    "prioridade": "ALTA",
    "prazo": "2026-11-20"
  }'
```

**Resposta:**
```json
{
  "id": 1,
  "projeto": 1,
  "titulo": "Criar tela de login",
  "descricao": "",
  "status": "PENDENTE",
  "prioridade": "ALTA",
  "prazo": "2026-11-20",
  "data_criacao": "2026-11-10T17:05:00Z",
  "data_atualizacao": "2026-11-10T17:05:00Z"
}
```

### 3. Exemplo de Violação de Regra de Negócio (Título com menos de 3 caracteres)

```bash
curl -X POST http://127.0.0.1:8000/tarefas/ \
  -H "Content-Type: application/json" \
  -d '{
    "projeto": 1,
    "titulo": "Oi"
  }'
```

**Resposta de Erro (`400 Bad Request`):**
```json
{
  "titulo": [
    "O título da tarefa deve ter, no mínimo, 3 caracteres."
  ]
}
```

### 4. Atualizar o Status de uma Tarefa (`PATCH`)

```bash
curl -X PATCH http://127.0.0.1:8000/tarefas/1/ \
  -H "Content-Type: application/json" \
  -d '{
    "status": "CONCLUIDA"
  }'
```

---

## Estrutura do Repositório

```text
django-quickproject/
├── config/                  # Configurações globais do Django (settings, urls, asgi, wsgi)
├── docs/                    # Documentação e artefatos de engenharia
│   ├── diagrama.iuml        # Diagrama de classes em PlantUML
│   └── testes-api-tasks.md  # Documentação detalhada dos testes automatizados
├── tasks/                   # Aplicação principal de Gerenciamento de Tarefas
│   ├── api/
│   │   ├── serializers.py   # Serializers do DRF (ProjetoSerializer, TarefaSerializer)
│   │   └── views.py         # ViewSets do DRF (ProjetoViewSet, TarefaViewSet)
│   ├── migrations/          # Migrações do banco de dados SQLite
│   ├── apps.py              # Configuração da app tasks
│   ├── models.py            # Modelos Projeto, Tarefa e Enums StatusTarefa, Prioridade
│   └── tests.py             # Testes automatizados da API de tarefas (APITestCase)
├── users/                   # Aplicação de usuários e perfis
│   ├── api/
│   │   ├── serializers.py   # Serializer de UserProfile
│   │   └── views.py         # ViewSet de UserProfile
│   ├── admin.py             # Registro no admin
│   ├── models.py            # Modelo UserProfileExample
│   └── tests.py             # Testes de exemplo da aplicação users
├── db.sqlite3               # Banco de dados SQLite local
├── manage.py                # Utilitário de linha de comando do Django
├── pytest.ini               # Configuração do executor pytest
├── requirements.txt         # Lista de dependências do projeto
└── README.md                # Documentação do projeto (este arquivo)
```
