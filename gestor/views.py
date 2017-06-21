from django.shortcuts import get_object_or_404

from rest_framework.exceptions import PermissionDenied
from rest_framework.exceptions import ValidationError

from rest_framework.parsers import JSONParser
from rest_framework.parsers import MultiPartParser

from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework.response import Response

from rest_framework.viewsets import ViewSet
from rest_framework.viewsets import ModelViewSet

from oidc_auth.authentication import JSONWebTokenAuthentication

from core.views import DefaultMixin
from core.views import MultiSerializerViewSet

from .models import Gestor
from .models import ProcessoVinculacao
from .models import ArquivosProcessoVinculacao

from .serializers import GestorSerializer
from .serializers import GestorListSerializer
from .serializers import ProcessoVinculacaoSerializer
from .serializers import ProcessoVinculacaoListSerializer
from .serializers import ProcessoVinculacaoDetailSerializer
from .serializers import ArquivosProcessoVinculacaoSerializer
from .serializers import RegistroProcessoVinculacaoSerializer

from .permissions import CommonUserOrReadOnly
from .permissions import IsManagerOrReadOnly


class GestorViewSet(DefaultMixin, MultiSerializerViewSet, ModelViewSet):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsManagerOrReadOnly, )

    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer

    serializers = {
        'list': GestorListSerializer,
    }

    filter_fields = ('praca', 'atual')


class ProcessoViewSet(DefaultMixin, MultiSerializerViewSet, ModelViewSet):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (CommonUserOrReadOnly, )

    queryset = ProcessoVinculacao.objects.all()
    serializer_class = ProcessoVinculacaoSerializer
    serializers = {
        'list': ProcessoVinculacaoListSerializer,
        'retrieve': ProcessoVinculacaoDetailSerializer,
    }

    filter_fields = ('praca', 'aprovado', 'finalizado')

    def partial_update(self, request, pk=None):
        processo = get_object_or_404(ProcessoVinculacao, pk=pk)

        self.check_object_permissions(request, processo)

        if 'situacao' in request.data:
            situacao = {
                "situacao": request.data.pop('situacao'),
                "descricao": request.data.pop('descricao'),
            }
            serializer = RegistroProcessoVinculacaoSerializer(
                data=situacao)
            if serializer.is_valid():
                serializer.save(processo=processo)
                serializer = ProcessoVinculacaoDetailSerializer(processo, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
                else:
                    raise ValidationError(serializer.errors)
            else:
                raise ValidationError(serializer.errors)

        serializer = ProcessoVinculacaoDetailSerializer(processo,
                                                        data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise ValidationError(serializer.errors)


class ArquivoProcessoViewSet(DefaultMixin, ViewSet):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (CommonUserOrReadOnly, )

    parser_classes = (JSONParser, MultiPartParser)
    queryset = ArquivosProcessoVinculacao.objects.all()

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
        return Response(serializer.data)

    def partial_update(self, request, pk=None, processo_pk=None):
        arquivo = get_object_or_404(ArquivosProcessoVinculacao, pk=pk)

        self.check_object_permissions(request, arquivo)
        serializer = ArquivosProcessoVinculacaoSerializer(
            arquivo, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise PermissionDenied
