import json

from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from core.models import Praca, Gestor, ProcessoAdmissao

from .serializers import (
        PracaSerializer, 
        PracaListSerializer,
        GestorSerializer,
        ProcessoAdmissaoSerializer
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

    serializers = {
            'list': PracaListSerializer,
            }



class GestorViewSet(ModelViewSet):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer


class ProcessoViewSet(DefaultMixin, ModelViewSet):
    queryset = ProcessoAdmissao.objects.all()
    serializer_class = ProcessoAdmissaoSerializer
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
