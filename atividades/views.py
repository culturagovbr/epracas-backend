from rest_framework.viewsets import ModelViewSet

from core.views import DefaultMixin

from .models import Agenda
from .serializers import AgendaSerializer


class AgendaViewSet(DefaultMixin, ModelViewSet):
    partial = True
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer
