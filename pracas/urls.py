from django.conf.urls import include, url

from rest_framework_nested import routers

from .views import PracaViewSet
from .views import DistanceView
from .views import GrupoGestorViewSet

from .views import ImagemPracaViewSet

from .views import ParceiroViewSet


router = routers.SimpleRouter()

router.register(r'pracas', PracaViewSet)
router.register(r'grupogestor', GrupoGestorViewSet)

imagem_router = routers.NestedSimpleRouter(router, r'pracas', lookup='praca')
imagem_router.register(r'imagens', ImagemPracaViewSet)

parceiro_router = routers.NestedSimpleRouter(router, r'pracas', lookup='praca')
parceiro_router.register(r'parceiros', ParceiroViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(imagem_router.urls)),
    url(r'^', include(parceiro_router.urls)),
    url(r'^distancia/$', DistanceView.as_view(), name='distancia'),
]
