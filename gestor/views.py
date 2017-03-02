from django.shortcuts import get_object_or_404

from rest_framework.exceptions import PermissionDenied

from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser

from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.response import Response

from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet

from oidc_auth.authentication import JSONWebTokenAuthentication

from core.views import DefaultMixin

from .models import Gestor
from .models import ProcessoVinculacao
from .models import ArquivosProcessoVinculacao

from .serializers import GestorSerializer
from .serializers import ProcessoVinculacaoSerializer
from .serializers import ArquivosProcessoVinculacaoSerializer

from .permissions import CommonUserOrReadOnly


class GestorViewSet(ModelViewSet):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAuthenticatedOrReadOnly, )

    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


class ProcessoViewSet(DefaultMixin, ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (CommonUserOrReadOnly, )

    queryset = ProcessoVinculacao.objects.all()
    serializer_class = ProcessoVinculacaoSerializer
    search_fields = ('gestor', 'praca')


class ArquivoProcessoViewSet(DefaultMixin, ViewSet):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (CommonUserOrReadOnly, )

    parser_classes = (JSONParser, MultiPartParser)

    def list(self, request, processo_pk=None):
        processo = get_object_or_404(ProcessoVinculacao, pk=processo_pk)

        arquivos = ArquivosProcessoVinculacao.objects.filter(processo=processo)

        serializer = ArquivosProcessoVinculacaoSerializer(arquivos, many=True)
        return Response(serializer.data)

    def create(self, request, processo_pk=None):
        processo = get_object_or_404(ProcessoVinculacao, pk=processo_pk)
        if request.user != processo.user:
            raise PermissionDenied

        for tipo in request.FILES:
            arquivo = ArquivosProcessoVinculacao(
                processo=processo, tipo=tipo, arquivo=request.FILES[tipo])
            arquivo.clean_fields()
            arquivo.save()

        arquivos = ArquivosProcessoVinculacao.objects.filter(processo=processo)
        serializer = ArquivosProcessoVinculacaoSerializer(arquivos, many=True)

        return Response(serializer.data)

    def retrieve(self, request, pk=None, processo_pk=None):
        processo = get_object_or_404(ProcessoVinculacao, pk=processo_pk)

        arquivo = get_object_or_404(ArquivosProcessoVinculacao, pk=pk)

        serializer = ArquivosProcessoVinculacaoSerializer(arquivo)
        if serializer.is_valid():
            return Response(serializer.data)
