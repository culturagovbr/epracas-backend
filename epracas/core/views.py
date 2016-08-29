from rest_framework.viewsets import ModelViewSet

from .models import Praca, Gestor, ProcessoAdmissao
from .serializers import (
        PracaSerializer, 
        GestorSerializer,
        ProcessoAdmissaoSerializer
        )


class PracaViewSet(ModelViewSet):
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer


class GestorViewSet(ModelViewSet):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


class ProcessoViewSet(ModelViewSet):
    queryset = ProcessoAdmissao.objects.all()
    serializer_class = ProcessoAdmissaoSerializer
