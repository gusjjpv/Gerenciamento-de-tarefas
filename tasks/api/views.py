"""Views for the tasks app using Django REST Framework viewsets."""

from rest_framework import viewsets
from .serializers import ProjetoSerializer, TarefaSerializer
from ..models import Projeto, Tarefa

class ProjetoViewSet(viewsets.ModelViewSet):
    """CRUD operations for Projeto."""
    queryset = Projeto.objects.all()
    serializer_class = ProjetoSerializer

class TarefaViewSet(viewsets.ModelViewSet):
    """CRUD operations for Tarefa."""
    queryset = Tarefa.objects.all()
    serializer_class = TarefaSerializer
