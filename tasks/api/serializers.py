"""Serializers for the tasks app."""

from rest_framework import serializers
from ..models import Projeto, Tarefa

class ProjetoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Projeto
        fields = [
            "id",
            "usuario",
            "nome",
            "descricao",
            "data_criacao",
            "data_atualizacao",
        ]
        read_only_fields = ["data_criacao", "data_atualizacao"]

class TarefaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarefa
        fields = [
            "id",
            "projeto",
            "titulo",
            "descricao",
            "status",
            "prioridade",
            "prazo",
            "data_criacao",
            "data_atualizacao",
        ]
        read_only_fields = ["data_criacao", "data_atualizacao"]
