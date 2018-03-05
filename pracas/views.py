from datetime import date

from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from oidc_auth.authentication import JSONWebTokenAuthentication

from core.views import DefaultMixin
from core.views import MultiSerializerViewSet
from core.metadata import ChoicesMetadata

from .models import Praca
from .models import Parceiro
from .models import GrupoGestor
from .models import MembroGestor
from .models import ImagemPraca
from .models import MembroUgl
from .models import Rh
from .models import Ator

from .serializers import PracaSerializer
from .serializers import PracaListSerializer
from .serializers import ImagemPracaSerializer
from .serializers import DistanciaSerializer
from .serializers import GrupoGestorSerializer
from .serializers import MembroGestorSerializer
from .serializers import MembroGestorDetailSerializer
from .serializers import ParceiroDetailSerializer
from .serializers import MembroUglSerializer
from .serializers import RhDetailSerializer
from .serializers import RhListSerializer
from .serializers import AtorDetailSerializer

from .permissions import IsAdminOrManagerOrReadOnly
from .permissions import IsOwnerOrReadOnly


class PracaViewSet(DefaultMixin, MultiSerializerViewSet):

    authentication_classes = (JSONWebTokenAuthentication, )
    permission_classes = (IsAdminOrManagerOrReadOnly, )

    metadata_class = ChoicesMetadata
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
        praca = get_object_or_404(Praca, pk=praca_pk)
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

    def list(self, request, praca_pk=None):
        if not praca_pk:
            imagens = ImagemPraca.objects.all()
            serializer = ImagemPracaSerializer(imagens, many=True)

            return Response(serializer.data, status=200)

        praca = get_object_or_404(Praca, pk=praca_pk)
        imagens = praca.imagem.all()
        serializer = ImagemPracaSerializer(imagens, many=True)

        return Response(serializer.data, status=200)

    def partial_update(self, request, pk=None, praca_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        imagem = get_object_or_404(ImagemPraca, pk=pk)

        self.check_object_permissions(request, praca)
        serializer = ImagemPracaSerializer(imagem, data=request.data,
                                           partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            raise ValidationError(serializer.errors)


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
        else:
            return Response(parceiro.errors, status=400)


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

    def list(self, request, praca_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)

        gg = GrupoGestor.objects.filter(praca=praca)
        serializer = GrupoGestorSerializer(gg, many=True)
        return Response(serializer.data)

    def destroy(self, request, praca_pk=None, pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        gg = get_object_or_404(GrupoGestor, pk=pk)
        
        gg.data_finalizacao = request.data['data_finalizacao']
        gg.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

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
    
    def list(self, request, praca_pk=None, grupogestor_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)

        gg = get_object_or_404(GrupoGestor, pk=grupogestor_pk, praca=praca)

        membros = MembroGestor.objects.filter(grupo_gestor=gg, data_desligamento=None)
        serializer = MembroGestorDetailSerializer(membros, many=True)
        return Response(serializer.data)

    def partial_update(self, request, praca_pk=None, grupogestor_pk=None, pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        gg = get_object_or_404(GrupoGestor, pk=grupogestor_pk, praca=praca)
        
        membro = get_object_or_404(MembroGestor, pk=pk)

        serializer = MembroGestorSerializer(membro, data=request.data,
                                           partial=True)
        
        if serializer.is_valid():
            serializer.save(grupo_gestor=gg)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, praca_pk=None, grupogestor_pk=None, pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        gg = get_object_or_404(GrupoGestor, pk=grupogestor_pk)

        membro = get_object_or_404(MembroGestor, pk=pk)

        membro.data_desligamento = request.data['data_desligamento']
        membro.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


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
    
    def list(self, request, praca_pk=None, unidadegestora_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)

        ugl = MembroUgl.objects.filter(praca=praca)

        serializer = MembroUglSerializer(ugl, many=True)
        return Response(serializer.data)


class RhViewSet(DefaultMixin, ModelViewSet):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    serializer_class = RhListSerializer
    queryset = Rh.objects.all()

    def create(self, request, praca_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        rh = RhDetailSerializer(data=request.data)
        if rh.is_valid():
            rh.save(praca=praca)
            return Response(rh.data, status=status.HTTP_201_CREATED)
        else:
            return Response(rh.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request, praca_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)

        rhs = Rh.objects.filter(praca=praca)
        serializer = RhDetailSerializer(rhs, many=True)
        return Response(serializer.data)

    def partial_update(self, request, praca_pk=None, pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        rh = get_object_or_404(Rh, pk=pk)

        rh_serializer = RhDetailSerializer(rh, data=request.data,
                                           partial=True)
        if rh_serializer.is_valid():
            rh_serializer.save(praca=praca)
            return Response(rh_serializer.data, status=status.HTTP_200_OK)
        return Response(rh_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def destroy(self, request, praca_pk=None, pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        rh = get_object_or_404(Rh, pk=pk)

        try:
            if request.data['excluir'] is True:
                rh.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except:
            if not request.data:
                rh.data_saida = date.today()
                rh.save()
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                serializer = RhDetailSerializer(rh, data=request.data, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response(serializer.errors,
                                    status=status.HTTP_400_BAD_REQUEST)


class AtorViewSet(DefaultMixin, ModelViewSet):

    authentication_classes = (JSONWebTokenAuthentication,)
    permission_classes = (IsOwnerOrReadOnly,)

    serializer_class = AtorDetailSerializer
    queryset = Ator.objects.all()

    def create(self, request, praca_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        ator = AtorDetailSerializer(data=request.data)
        if ator.is_valid():
            ator.save(praca=praca)
            return Response(ator.data, status=status.HTTP_201_CREATED)
        else:
            return Response(ator.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request, praca_pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)

        atores = Ator.objects.filter(praca=praca)
        serializer = AtorDetailSerializer(atores, many=True)
        return Response(serializer.data)

    def destroy(self, request, praca_pk=None, pk=None):
        praca = get_object_or_404(Praca, pk=praca_pk)
        self.check_object_permissions(request, praca)

        ator = get_object_or_404(Ator, pk=pk)

        ator.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
