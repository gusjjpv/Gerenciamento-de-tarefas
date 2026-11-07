"""Serializers for the tasks app."""

from rest_framework import serializers
from ..models import MENSAGEM_TITULO_CURTO, TITULO_TAMANHO_MINIMO, Projeto, Tarefa

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

    def validate_titulo(self, value):
        # Business rule: title min 3 chars (returns 400 instead of 500)
        if len(value) < TITULO_TAMANHO_MINIMO:
            raise serializers.ValidationError(MENSAGEM_TITULO_CURTO)
        return value
