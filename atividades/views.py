from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ViewSet

from core.views import DefaultMixin

from .models import Agenda
from .models import Relatorio
from .models import RelatorioImagem

from .serializers import AgendaDetailSerializer
from .serializers import RelatorioSerializer
from .serializers import RelatorioImagemSerializer


class AgendaViewSet(DefaultMixin, ModelViewSet):

    serializer_class = AgendaDetailSerializer
    partial = True
    queryset = Agenda.objects.all()


class RelatorioViewSet(DefaultMixin, ViewSet):

    serializer_class = RelatorioSerializer

    def list(self, request, agenda_pk=None):
        queryset = Relatorio.objects.filter(agenda=agenda_pk)
        serializer = RelatorioSerializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, agenda_pk=None):
        agenda = Agenda.objects.get(id_pub=agenda_pk)
        serializer = RelatorioSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            relatorio = Relatorio.objects.create(agenda=agenda, **serializer.data)
            serializer = RelatorioSerializer(relatorio)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class RelatorioImagensViewSet(DefaultMixin, ViewSet):

    serializer_class = RelatorioImagemSerializer

    def list(self, request, agenda_pk=None, relatorio_pk=None):
        queryset = RelatorioImagem.objects.filter(pk=relatorio_pk)
        serializer = RelatorioImagemSerializer(queryset, many=True)

        return Response(serializer.data)

    def create(self, request, agenda_pk=None, relatorio_pk=None):
        relatorio = Relatorio.objects.get(pk=relatorio_pk)

        if request.FILES:
            for afile in request.FILES.getlist('arquivo'):
                RelatorioImagem.objects.create(relatorio=relatorio, arquivo=afile)

        queryset = RelatorioImagem.objects.filter(relatorio=relatorio)
        serializer = RelatorioImagemSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
