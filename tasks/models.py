"""Models for task management app.

Based on the diagram in docs/diagrama.iuml we have:
- Projeto (Project) linked to a User (owner)
- Tarefa (Task) linked to a Projeto
- Enums for status and priority

Business rules:
- title must have at least 3 characters
- default status is PENDENTE when creating a Tarefa without explicit status
"""

from django.db import models
from django.contrib.auth.models import User

class StatusTarefa(models.TextChoices):
    PENDENTE = "PENDENTE", "Pendente"
    EM_ANDAMENTO = "EM_ANDAMENTO", "Em andamento"
    CONCLUIDA = "CONCLUIDA", "Concluída"

class Prioridade(models.TextChoices):
    BAIXA = "BAIXA", "Baixa"
    MEDIA = "MEDIA", "Média"
    ALTA = "ALTA", "Alta"

class Projeto(models.Model):
    """Projeto pertence a um usuário (owner)."""
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projetos")
    nome = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome

class Tarefa(models.Model):
    """Tarefa vinculada a um Projeto."""
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name="tarefas")
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=StatusTarefa.choices,
        default=StatusTarefa.PENDENTE,
    )
    prioridade = models.CharField(
        max_length=10,
        choices=Prioridade.choices,
        default=Prioridade.MEDIA,
    )
    prazo = models.DateField(null=True, blank=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def clean(self):
        # Business rule: title min 3 chars
        if len(self.titulo) < 3:
            raise models.ValidationError({"titulo": "O título da tarefa deve ter, no mínimo, 3 caracteres."})

    def save(self, *args, **kwargs):
        # Ensure clean is called on save
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
