from django.shortcuts import get_object_or_404

from rest_framework.parsers import MultiPartParser
from rest_framework.parsers import FormParser
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from oidc_auth.authentication import JSONWebTokenAuthentication

from core.views import DefaultMixin
from core.views import MultiSerializerViewSet

from gestor.models import ProcessoVinculacao
from gestor.models import ArquivosProcessoVinculacao
from gestor.serializers import ProcessoVinculacaoSerializer

from .models import Praca
from .models import Parceiro
from .models import GrupoGestor
from .models import ImagemPraca

from .serializers import PracaSerializer
from .serializers import PracaListSerializer
from .serializers import ImagemPracaSerializer
# from .serializers import HeaderUploadSerializer
from .serializers import DistanciaSerializer
from .serializers import GrupoGestorSerializer

from .serializers import ParceiroSerialier

from .permissions import IsAdminOrManagerOrReadOnly


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

    serializer_class = ImagemPracaSerializer
    queryset = ImagemPraca.objects.all()

    def create(self, request, praca_pk=None):
        praca = Praca.objects.get(pk=praca_pk)

        file_list = []
        if request.FILES:
            for afile in request.FILES.getlist('arquivo'):
                file_list.append(ImagemPraca.objects.create(praca=praca,
                                                            **request.data))

        serializer = ImagemPracaSerializer(file_list, many=True)
        return Response(serializer.data, status=201)



class PracaUploadHeader(DefaultMixin, APIView):

    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request, pk):
        praca = get_object_or_404(Praca, pk=pk)
        praca.header_img = request.FILES['header_img']
        praca.clean_fields()
        praca.save()

        serializer = HeaderUploadSerializer(
                praca,
                context={'request': request})
        return Response(serializer.data)


class PracaVinculoUpload(DefaultMixin, APIView):

    parser_classes = (JSONParser, MultiPartParser, FormParser)
    authentication_classes = (JSONWebTokenAuthentication,)

    def post(self, request, pk):
        user = request.user
        praca = get_object_or_404(Praca, pk=pk)

        processo, created = ProcessoVinculacao.objects.get_or_create(
            praca=praca,
            defaults={'user': user, 'praca': praca}
            )

        for tipo in request.FILES:
            arq = ArquivosProcessoVinculacao(
                processo=processo,
                tipo=tipo,
                arquivo=request.FILES[tipo])
            arq.clean_fields()
            arq.save()

        serializer = ProcessoVinculacaoSerializer(
            processo,
            context={'request': request})
        return Response(serializer.data)


class DistanceView(DefaultMixin, APIView):

    def post(self, request, latlong=None):
        latlong = (request.data['lat'], request.data['long'])
        distancias = sorted(
                [
                    (praca, praca.get_distance(latlong))
                    for praca in Praca.objects.all()
                ],
                key=lambda distancia: distancia[1]
                )
        pracas = [praca for (praca, distancia) in distancias[:5]]

        serializer = DistanciaSerializer(pracas, context={'origem': latlong,
                                                          'request': request}, many=True)


        return Response(serializer.data)


class ParceiroViewSet(DefaultMixin, ModelViewSet):

    serializer_class = ParceiroSerialier
    queryset = Parceiro.objects.all()
    # search_fields = ('nome', 'municipio', 'uf')

    # serializers = {
    #         'list': PracaListSerializer,
    #         }


class GrupoGestorViewSet(DefaultMixin, ModelViewSet):

    serializer_class = GrupoGestorSerializer
    queryset = GrupoGestor.objects.all()
