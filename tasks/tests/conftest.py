"""Fixtures compartilhadas pelos testes do app tasks."""

import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from tasks.models import Projeto, Tarefa


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def usuario(db):
    return User.objects.create_user(username="dono", password="senha-teste-123")


@pytest.fixture
def outro_usuario(db):
    return User.objects.create_user(username="outro", password="senha-teste-456")


@pytest.fixture
def projeto(usuario):
    return Projeto.objects.create(usuario=usuario, nome="Projeto Alpha", descricao="Desc")


@pytest.fixture
def tarefa(projeto):
    return Tarefa.objects.create(projeto=projeto, titulo="Primeira tarefa")
