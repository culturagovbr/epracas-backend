from rest_framework.viewsets import ModelViewSet

from .models import Praca, Gestor
from .serializers import PracaSerializer, GestorSerializer


class PracaViewSet(ModelViewSet):
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer


class GestorViewSet(ModelViewSet):
    queryset = Gestor.objects.all()
    serializer_class = GestorSerializer
