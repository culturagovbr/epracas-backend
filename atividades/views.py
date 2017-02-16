from rest_framework.viewsets import ModelViewSet

from core.views import DefaultMixin

from .models import Agenda
from .models import Relatorio

from .serializers import AgendaDetailSerializer
from .serializers import RelatorioSerializer


class AgendaViewSet(DefaultMixin, ModelViewSet):

    serializer_class = AgendaDetailSerializer
    partial = True
    queryset = Agenda.objects.all()


class RelatorioViewSet(DefaultMixin, ModelViewSet):

    serializer_class = RelatorioSerializer
    partial = True
    queryset = Relatorio.objects.all()
