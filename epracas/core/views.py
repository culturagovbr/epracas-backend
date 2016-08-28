from rest_framework.viewsets import ModelViewSet

from .models import Praca
from .serializers import PracaSerializer


class PracaViewSet(ModelViewSet):
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer
