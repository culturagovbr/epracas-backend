from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from core.views import DefaultMixin

from datetime import date

from .models import Agenda, Relatorio
from .serializers import AgendaSerializer, RelatorioSerializer


class AgendaViewSet(DefaultMixin, ModelViewSet):
    partial = True
    queryset = Agenda.objects.all()
    serializer_class = AgendaSerializer

    def get(self, request):

        ano = request.query_params.get('ano', False)
        mes = request.query_params.get('mes', False)

        if mes and ano:
           agenda_list = Agenda.objects.for_period(from_date=date(ano, mes),
                                                    to_date=date(ano, mes))
        else:
            agenda_list = Agenda.objects.all()

        response = serializer_class(agenda_list, many=True).data
        return Response(response)

    def patch(self, request, pk):

        agenda = Agenda.objects.get(id_pub = pk)

        # TODO: melhorar aqui usando RelatorioSerializer
        relatorio = RelatorioSerializer(
            agenda = agenda,
            data = request.data
        )
        if relatorio.is_valid():
            relatorio.save()
            Response(relatorio.data)
        else:
            Response(status.HTTP_400_BAD_REQUEST)
