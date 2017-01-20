from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from core.views import DefaultMixin

from .models import Agenda
from .serializers import AgendaSerializer


class AgendaViewSet(DefaultMixin, ModelViewSet):
    partial = True
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    def get(self, request):
        agenda_list = Agenda.objects.all()
        response = serializer_class(agenda_list, many=True).data

        return Response(response)
