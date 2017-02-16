from rest_framework.viewsets import ModelViewSet

from core.views import DefaultMixin

from .models import Agenda

from .serializers import AgendaDetailSerializer


class AgendaViewSet(DefaultMixin, ModelViewSet):

    serializer_class = AgendaDetailSerializer
    partial = True
    queryset = Agenda.objects.all()
