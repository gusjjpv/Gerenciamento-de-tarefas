### Bem-vindo ao DRF Quick Project!

Nesta experiência de aprendizado interativa, você aprenderá uma breve visão sobre o desenvolvimento de Web APIs com Django Rest Framework (DRF). Seja você iniciante em Django ou já familiarizado com ele, este projeto fornecerá uma abordagem prática e passo a passo para criar APIs RESTful rapidamente.

Neste projeto você explorará componentes essenciais do DRF, como serializers, views, autenticação e permissões, entre outros. Você também pode ver exemplos de testes unitários com pytest para garantir a confiabilidade dos endpoints da sua API. Ao final deste projeto, você terá uma boa compreensão de como o DRF funciona e o conhecimento básico para construir APIs com Django.

#### Django Rest Framework (DRF)

Django Rest Framework (DRF) é um toolkit poderoso e flexível para construção de Web APIs em Python utilizando o framework web Django. Ele fornece um conjunto abrangente de ferramentas e recursos que tornam mais fácil para os desenvolvedores criarem APIs RESTful robustas e eficientes.

Algumas características principais do Django Rest Framework incluem:

* **Serializers**: o DRF fornece serializers para converter dados complexos, como modelos Django, querysets ou objetos Python, em JSON ou XML para respostas da API. Eles também lidam com desserialização, permitindo que os dados sejam convertidos de volta para tipos nativos do Python para processamento.

* **Viewsets e Views**: o DRF oferece classes de views poderosas, como Viewsets e Views, que tratam a lógica para processar métodos HTTP como GET, POST, PUT, PATCH e DELETE em diferentes endpoints da API.

* **Autenticação e Permissões**: o DRF inclui vários métodos de autenticação, como Token Authentication, Basic Authentication e JSON Web Tokens (JWT), para proteger APIs. Ele também suporta permissões granulares para controlar o acesso aos recursos.

* **Paginação**: o DRF permite configuração simples de paginação para respostas da API, possibilitando o tratamento eficiente de grandes volumes de dados.

* **Filtragem, Busca e Ordenação**: o DRF fornece mecanismos de filtragem que facilitam a busca, filtragem e ordenação dos resultados da API, melhorando sua usabilidade.

De forma geral, o Django Rest Framework é amplamente adotado pela comunidade Python e Django devido à sua facilidade de uso, documentação extensa e versatilidade na construção de Web APIs escaláveis e de alta qualidade. Ele fornece uma base sólida para que desenvolvedores criem APIs RESTful com o mínimo de código repetitivo, permitindo foco na entrega de aplicações funcionais e ricas em recursos.

#### Requisitos do Sistema

Para construir aplicações web com DRF, você precisará dos seguintes requisitos em seu sistema:

* Python 3.10 ou versão mais recente;
* Pip 22.0 ou versão mais recente;
* Virtualenv 20.19 ou versão mais recente;

#### Instalação Rápida

Este guia tem como objetivo iniciar rapidamente as configurações do projeto e proporcionar uma experiência prática rápida com DRF. No entanto, para habilitar e executar o projeto, alguns comandos ainda são necessários.

* **Passo 1** - Crie um ambiente virtual Python para instalar todas as dependências necessárias:

```
    python3 -m venv venv
```

* **Passo 2** - Ative o ambiente virtual Python:

```
    . venv/bin/activate
```

* **Passo 3** - Instale todas as dependências:

```
    pip install -r requirements.txt
```

* **Passo 4** - Execute o servidor interno e divirta-se! ;)

```
    python manage.py runserver
```

Pare o servidor digitando Ctrl+C no terminal.

#### Arquitetura do DRF

A arquitetura do DRF é construída sobre a arquitetura consolidada do Django, que é um framework web de alto nível em Python. O DRF estende as capacidades do Django para fornecer uma arquitetura especializada para construção de Web APIs (Application Programming Interfaces), seguindo os princípios de Representational State Transfer (REST).

Aqui está uma breve descrição dos principais componentes da arquitetura do DRF:

1. **Serializers**: lidam com a conversão de dados entre tipos complexos e respostas da API.
2. **Views e Viewsets**: gerenciam o processamento das requisições da API e a geração de respostas.
3. **Roteamento de URLs**: mapeia URLs para as views ou viewsets apropriados.
4. **Autenticação e Permissões**: garantem a segurança da API com diferentes métodos de autenticação e controle granular de acesso.
5. **Paginação**: trata eficientemente grandes volumes de dados configurando paginação nas respostas da API.
6. **Negociação de Conteúdo**: responde com diferentes tipos de conteúdo com base nas requisições do cliente.
7. **Filtragem, Busca e Ordenação**: habilita filtragem, busca e ordenação dos resultados da API.
8. **Versionamento de API**: suporta mudanças na API mantendo compatibilidade com versões anteriores.

#### Estrutura de Diretórios

A estrutura de diretórios do DRF é semelhante à de um projeto Django padrão. No entanto, o DRF introduz alguns diretórios e arquivos específicos essenciais para a construção de Web APIs.

**Diretório Raiz do Projeto**:

* É o diretório principal do projeto DRF.
* Contém o arquivo principal de configuração do projeto, geralmente chamado `settings.py`, onde são definidas as configurações globais.
* Também inclui outros arquivos de configuração como `urls.py`, que define os padrões de URL do projeto.

**Diretórios de Aplicações (Apps)**:

* O DRF segue a arquitetura baseada em apps do Django, onde cada app representa uma funcionalidade específica.
* Cada app normalmente contém seus próprios arquivos `models.py`, `views.py` e `serializers.py`.
* O arquivo `models.py` define os modelos de dados.
* O arquivo `views.py` contém as views e viewsets para manipular requisições e respostas da API.
* O arquivo `serializers.py` define os serializers para conversão de dados.

Exemplo:

```
project_root/
|-- config/
|   |-- __init__.py
|   |-- asgi.py
|   |-- settings.py
|   |-- urls.py
|   |-- wsgi.py
|
|-- users/
|   |-- api/
|       |-- views.py
|       |-- serializers.py
|   |-- migrations/
|   |-- __init__.py
|   |-- admin.py
|   |-- apps.py
|   |-- models.py
|   |-- tests.py
|   |-- views.py
|-- .gitignore
|-- db.sqlite3 (banco de dados local com SQLite)
|-- LICENSE
|-- manage.py
|-- README.md (Este arquivo!)
|-- requirements.txt (opcional)
```

#### Criando Apps

O DRF fornece uma estratégia simples de modularização com apps. Para criar uma nova app no seu projeto, digite:

```
   django-admin startapp new_app_name
```

Vamos iniciar nosso projeto tutorial para uma livraria (Bookstore). Adicionaremos uma app chamada **books**.

```
   django-admin startapp books
```

Todas as apps precisam ser incluídas na variável `INSTALLED_APPS` em **config/settings.py**.

```python
# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework.authtoken",
    "users",
    "books", # <--- Nossa app aqui
]
```

#### Modelos Django (ORM)

O DRF utiliza o poderoso sistema ORM (Object-Relational Mapping) do Django para interagir com bancos de dados e gerenciar persistência de dados em Web APIs. O ORM do DRF se baseia no ORM do Django, permitindo que desenvolvedores trabalhem com recursos da API como objetos Python e realizem facilmente operações CRUD (Create, Retrieve, Update, Delete) no banco de dados.

Para incluir novos modelos em nossa Bookstore, vamos adicionar o modelo `Book` no arquivo **books/models.py**.

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    def __str__(self):
        return self.title
```

Após criar nosso modelo `Book`, precisamos atualizar a estrutura do banco de dados para incluir o novo modelo.

Digite os comandos:

```
   python manage.py makemigrations
```

```
   python manage.py migrate
```

### Interface Admin do Django

A interface Admin do Django é uma ferramenta poderosa e amigável que já vem integrada ao framework Django. Ela fornece uma interface web fácil de usar para gerenciar e interagir com os dados da aplicação.

Adicione os seguintes comandos para registrar o novo modelo no admin. No arquivo **books/admin.py**, adicione:

```python
from django.contrib import admin
from books.models import Book  # <--- importa o modelo

# Register your models here.

admin.site.register(Book)  # <--- registra o modelo
```

#### Serializers no DRF

Os serializers desempenham um papel crucial ao facilitar a conversão de dados entre tipos complexos do Python e representações da API, como JSON ou XML.

Para incluir os serializers, vamos criar um novo diretório chamado **api** dentro de **books**, e criar um novo arquivo chamado **serializers.py**.

O caminho será **books/api/serializers.py**.

Adicione as seguintes linhas:

```python
from rest_framework import serializers
from books.models import Book

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author']
```

#### Views no DRF e Class-Based Views

O DRF fornece duas abordagens principais para tratar requisições e respostas da API: function-based views e class-based views. As class-based views são mais sofisticadas e preferidas devido à modularidade e reutilização de código.

Exemplo de Function-based View:

```python
from rest_framework.decorators import api_view
from rest_framework.response import Response
from books.models import Book
from books.api.serializers import BookSerializer

@api_view(['GET', 'POST'])
def book_list_create_view(request):
    if request.method == 'GET':
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
```

Agora vamos incluir uma Class-based View para listar livros. Crie o arquivo **views.py** em **books/api**.

Adicione:

```python
from rest_framework.viewsets import ModelViewSet
from books.models import Book
from books.api.serializers import BookSerializer

class BookListCreateView(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
```

#### Roteamento no DRF

O roteamento é um componente essencial que mapeia URLs para views ou viewsets apropriadas em uma Web API.

Vamos incluir nossa view para listar livros no arquivo **config/urls.py**:

```python
from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken import views
from books.api.views import BookListCreateView ### View de Book

from users.api.views import UserProfileExampleViewSet

router = SimpleRouter()

router.register("users", UserProfileExampleViewSet, basename="users")
router.register("api/books", BookListCreateView, basename="book-list"), ## <-- rota da listagem de livros

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/token-auth/", views.obtain_auth_token),
]+router.urls
```

Pronto! Agora execute o servidor interno com o comando:

```
   python manage.py runserver
```

#### Interface Admin do Django

Para acessar a interface administrativa do Django, digite a seguinte URL no navegador:

```
http://localhost:8000/admin/
```

No formulário de login, use as credenciais:

```
login: admin
password: adminadmin
```

Na tela, procure o item **Books** na lista. Em seguida, no canto superior direito, clique em **ADD BOOK +**. Aparecerá um formulário para cadastrar novos livros no sistema.

Para acessar a lista de livros, digite:

```
http://localhost:8000/api/books/
```

#### Autenticação por Token

Configuramos a autenticação nativa por token do DRF. Para obter um token, use o endpoint:

* **api/token-auth/** enviando credenciais válidas de usuário/senha.

As credenciais do usuário admin são `admin/adminadmin`.

Envie a seguinte requisição JSON:

```json
{
    "username": "admin",
    "password": "adminadmin"
}
```

Para incluir novos usuários, crie um novo endpoint para o modelo `User` ou adicione usuários pela Interface Admin do Django.

#### Managers e Services

Managers e Services desempenham papéis essenciais no gerenciamento de dados e lógica de negócio em Web APIs.

**Managers**: são parte fundamental do ORM do Django, fornecendo uma forma conveniente de encapsular lógica de consulta e operações de banco de dados.

Exemplo:

```python
## managers.py
from django.db import models

class PublishedBooksManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=True)
```

```python
## models.py
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    is_published = models.BooleanField(default=False)

    objects = models.Manager()  # Manager padrão
    published_books = PublishedBooksManager()  # Manager customizado
```

**Services**: são componentes de alto nível projetados para lidar com lógica de negócio complexa e atuar como intermediários entre views e models.

Exemplo:

```python
# services.py
from books.models import Book

class BookService:
    @staticmethod
    def calculate_total_price(book_ids):
        total_price = 0
        for book_id in book_ids:
            try:
                book = Book.objects.get(id=book_id)
                total_price += book.price
            except Book.DoesNotExist:
                pass
        return total_price
```

Juntos, Managers e Services melhoram a organização e eficiência de um projeto Django Rest Framework, promovendo separação clara de responsabilidades e facilitando o desenvolvimento de Web APIs robustas e escaláveis.

#### Testes no Django

O Django Rest Framework suporta testes unitários com `pytest`, um framework de testes popular na comunidade Python.

Exemplo:

```python
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from books.models import Book
from books.api.serializers import BookSerializer

class BookListViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('book-list-create')
        self.book1 = Book.objects.create(title='Book 1', author='Author 1')
        self.book2 = Book.objects.create(title='Book 2', author='Author 2')
        self.expected_data = BookSerializer([self.book1, self.book2], many=True).data

    def test_list_books(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, self.expected_data)
```

Para executar os testes, use o comando:

```
    pytest
```

Bons estudos! Para mais informações, consulte a documentação oficial do DRF:

[Django Rest Framework Documentation](https://www.django-rest-framework.org/?utm_source=chatgpt.com)

Equipe LISA
_
# Gerenciamento-de-tarefas
