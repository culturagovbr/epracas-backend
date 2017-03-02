from django.shortcuts import get_object_or_404

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

    parser_classes = (JSONParser, MultiPartParser)

    # authentication_classes = (JSONWebTokenAuthentication,)

    def list(self, request, processo_pk=None):
        processo = get_object_or_404(ProcessoVinculacao, pk=processo_pk)

        arquivos = ArquivosProcessoVinculacao.objects.filter(processo=processo)

        serializer = ArquivosProcessoVinculacaoSerializer(arquivos, many=True)
        return Response(serializer.data)

    def create(self, request, processo_pk=None):
        processo = get_object_or_404(ProcessoVinculacao, pk=processo_pk)

        for tipo in request.FILES:
            arquivo = ArquivosProcessoVinculacao(
                processo=processo,
                tipo=tipo,
                arquivo=request.FILES[tipo])
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



    # def post(self, request, pk):
    #     user = request.user
    #     praca = get_object_or_404(Praca, pk=pk)

    #     processo, created = ProcessoVinculacao.objects.get_or_create(
    #         praca=praca,
    #         defaults={'user': user, 'praca': praca}
    #         )

    #     for tipo in request.FILES:
    #         arq = ArquivosProcessoVinculacao(
    #             processo=processo,
    #             tipo=tipo,
    #             arquivo=request.FILES[tipo])
    #         arq.clean_fields()
    #         arq.save()

    #     serializer = ProcessoVinculacaoSerializer(
    #         processo,
    #         context={'request': request})
    #     return Response(serializer.data)
