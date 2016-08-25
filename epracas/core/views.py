from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Praca
from .serializers import PracaSerializer


class PracaListView(ReadOnlyModelViewSet):
    queryset = Praca.objects.all()
    serializer_class = PracaSerializer
