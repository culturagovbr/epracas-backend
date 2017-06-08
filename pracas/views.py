from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from oidc_auth.authentication import JSONWebTokenAuthentication

from core.views import DefaultMixin
from core.views import MultiSerializerViewSet

from .models import Praca
from .models import Parceiro
from .models import GrupoGestor
from .models import MembroGestor
from .models import ImagemPraca
from .models import MembroUgl

from .serializers import PracaSerializer
from .serializers import PracaListSerializer
from .serializers import ImagemPracaSerializer
from .serializers import DistanciaSerializer
from .serializers import GrupoGestorSerializer
from .serializers import MembroGestorSerializer
from .serializers import ParceiroDetailSerializer
from .serializers import MembroUglSerializer

from .permissions import IsAdminOrManagerOrReadOnly
from .permissions import IsOwnerOrReadOnly


class PracaViewSet(DefaultMixin, MultiSerializerViewSet):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAdminOrManagerOrReadOnly, )

    serializer_class = PracaSerializer
    queryset = Praca.objects.all()
    search_fields = ('nome', 'municipio', 'uf')

    serializers = {
        'list': PracaListSerializer,
    }


class ImagemPracaViewSet(DefaultMixin, ModelViewSet):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    serializer_class = ImagemPracaSerializer
    queryset = ImagemPraca.objects.all()

    def create(self, request, praca_pk=None):
        praca = Praca.objects.get(pk=praca_pk)
        self.check_object_permissions(request, praca)

        try:
            if request.data['header']:
                praca.header_img = request.FILES['arquivo']
                praca.save()
                serializer = PracaListSerializer(praca)
        except:
            imagem = ImagemPracaSerializer(data=request.data)
            if imagem.is_valid():
                imagem.save(praca=praca)
                return Response(imagem.data, status=201)
            serializer = ImagemPracaSerializer(imagem)

        return Response(serializer.data, status=201)


class DistanceView(DefaultMixin, APIView):
    def post(self, request, latlong=None):
        latlong = (request.data['lat'], request.data['long'])
        distancias = sorted(
            [(praca, praca.get_distance(latlong))
             for praca in Praca.objects.all()],
            key=lambda distancia: distancia[1])
        pracas = [praca for (praca, distancia) in distancias[:5]]

        serializer = DistanciaSerializer(
            pracas, context={'origem': latlong,
                             'request': request}, many=True)

        return Response(serializer.data)


class ParceiroViewSet(DefaultMixin, ModelViewSet):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    serializer_class = ParceiroDetailSerializer
    queryset = Parceiro.objects.all()

    def create(self, request, praca_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        parceiro = ParceiroDetailSerializer(data=request.data)
        if parceiro.is_valid():
            parceiro.save(praca=praca)

            return Response(parceiro.data, status=201)


class GrupoGestorViewSet(DefaultMixin, ModelViewSet):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    serializer_class = GrupoGestorSerializer
    queryset = GrupoGestor.objects.all()

    def create(self, request, praca_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        gg = GrupoGestorSerializer(data=request.data)
        if gg.is_valid():
            gg.save(praca=praca)

            return Response(gg.data, status=status.HTTP_201_CREATED)
        else:
            return Response(gg.errors, status=status.HTTP_400_BAD_REQUEST)


class MembroGestorViewSet(DefaultMixin, ModelViewSet):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    serializer_class = MembroGestorSerializer
    queryset = MembroGestor.objects.all()

    def create(self, request, praca_pk=None, grupogestor_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        gg = get_object_or_404(GrupoGestor, pk=grupogestor_pk)

        membro = MembroGestorSerializer(data=request.data)
        if membro.is_valid(raise_exception=True):
            membro.save(grupo_gestor=gg)
            return Response(membro.data, status=status.HTTP_201_CREATED)
        else:
            return Response(membro.errors, status=status.HTTP_400_BAD_REQUEST)


class MembroUglViewSet(DefaultMixin, ModelViewSet):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    serializer_class = MembroUglSerializer
    queryset = MembroUgl.objects.all()

    def create(self, request, praca_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        membro = MembroUglSerializer(data=request.data)
        if membro.is_valid(raise_exception=True):
            membro.save(praca=praca)
            return Response(membro.data, status=status.HTTP_201_CREATED)
        else:
            return Response(membro.errors, status=status.HTTP_400_BAD_REQUEST)
