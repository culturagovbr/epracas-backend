from rest_framework.viewsets import ModelViewSet

from core.views import DefaultMixin

from .models import Gestor
from .models import ProcessoVinculacao

from .serializers import GestorSerializer
from .serializers import ProcessoVinculacaoSerializer


class GestorViewSet(ModelViewSet):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


class ProcessoViewSet(DefaultMixin, ModelViewSet):
    queryset = ProcessoVinculacao.objects.all()
    serializer_class = ProcessoVinculacaoSerializer
    search_fields = ('gestor', 'praca')
