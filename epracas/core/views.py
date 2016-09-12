from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from .models import Praca, Gestor, ProcessoAdmissao
from .serializers import (
        PracaSerializer, 
        GestorSerializer,
        ProcessoAdmissaoSerializer
        )


class DefaultMixin(object):
    filter_backends = (
            filters.DjangoFilterBackend,
            filters.SearchFilter,
            )

class PracaViewSet(DefaultMixin, ModelViewSet):
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer
    search_fields = (
            'municipio',
            'uf',
            'modelo',
            'situacao',
            )


class GestorViewSet(ModelViewSet):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


class ProcessoViewSet(DefaultMixin, ModelViewSet):
    queryset = ProcessoAdmissao.objects.all()
    serializer_class = ProcessoAdmissaoSerializer
    search_fields = ('gestor',)
