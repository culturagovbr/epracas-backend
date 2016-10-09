import json

from django.shortcuts import get_object_or_404

from rest_framework import filters
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import (
    JSONParser,
    MultiPartParser,
    FormParser,
    FileUploadParser
    )

from core.models import Praca, Gestor, ProcessoVinculacao

from .serializers import (
        PracaSerializer, 
        PracaListSerializer,
        PracaUploadSerializer,
        GestorSerializer,
        ProcessoVinculacaoSerializer,
        )


class DefaultMixin(object):
    filter_backends = (
            filters.DjangoFilterBackend,
            filters.SearchFilter,
            )


class MultiSerializerViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action in self.serializers:
            return self.serializers.get(
                    self.action,
                    self.serializers[self.action]
                    )
        else:
            return self.serializer_class


class PracaViewSet(DefaultMixin, MultiSerializerViewSet):

    serializer_class = PracaSerializer
    queryset = Praca.objects.all()
    parser_classes = (MultiPartParser, )

    serializers = {
            'list': PracaListSerializer,
            }


class PracaUploadHeader(DefaultMixin, APIView):

    parser_classes = (MultiPartParser, FormParser, )

    def post(self, request, pk):
        praca = get_object_or_404(Praca, pk=pk)
        praca.header_img = request.FILES['header_img']
        praca.clean_fields()
        praca.save()

        serializer = PracaUploadSerializer(
                praca,
                context={'request': request})
        return Response(serializer.data)


class GestorViewSet(ModelViewSet):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


class ProcessoViewSet(DefaultMixin, ModelViewSet):
    queryset = ProcessoVinculacao.objects.all()
    serializer_class = ProcessoVinculacaoSerializer
    search_fields = ('gestor',)


class DistanceView(DefaultMixin, APIView):

    def post(self, request, latlong=None):
        latlong = (request.data['lat'], request.data['long'])
        distancias = sorted(
                [(praca, praca.get_distance(latlong)) for praca in Praca.objects.all()],
                key = lambda distancia: distancia[1]
                )
        pracas = []

        for i in distancias[:5]:
            praca = {
                    'municipio': i[0].municipio,
                    'uf': i[0].uf,
                    'latlong': "{}, {}".format(i[0].lat, i[0].long),
                    'distancia': i[1]
                    }
            pracas.append(praca)

        return Response(pracas)
