from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from datetime import date

from core.views import DefaultMixin
from core.views import MultiSerializerViewSet


from .models import Agenda
from .models import Relatorio

from .serializers import AgendaDetailSerializer
from .serializers import RelatorioSerializer 


class AgendaViewSet(DefaultMixin, ModelViewSet):

    serializer_class = AgendaDetailSerializer
    partial = True
    queryset = Agenda.objects.all()
