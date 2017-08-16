from django.conf.urls import include, url

from rest_framework_nested import routers

from .views import PracaViewSet
from .views import DistanceView
from .views import GrupoGestorViewSet
from .views import MembroGestorViewSet
from .views import MembroUglViewSet
from .views import RhViewSet
from .views import AtorViewSet

from .views import ImagemPracaViewSet

from .views import ParceiroViewSet


router = routers.SimpleRouter()

router.register(r'pracas', PracaViewSet)

imagem_router = routers.NestedSimpleRouter(router, r'pracas', lookup='praca')
imagem_router.register(r'imagens', ImagemPracaViewSet)

parceiro_router = routers.NestedSimpleRouter(router, r'pracas', lookup='praca')
parceiro_router.register(r'parceiros', ParceiroViewSet)

grupogestor_router = routers.NestedSimpleRouter(router, r'pracas', lookup='praca')
grupogestor_router.register(r'grupogestor', GrupoGestorViewSet)

membrogestor_router = routers.NestedSimpleRouter(grupogestor_router, r'grupogestor', lookup='grupogestor')
membrogestor_router.register(r'membrogestor', MembroGestorViewSet)

membrougl_router = routers.NestedSimpleRouter(router, r'pracas', lookup='praca')
membrougl_router.register(r'unidadegestora', MembroUglViewSet)

rh_router = routers.NestedSimpleRouter(router, r'pracas', lookup='praca')
rh_router.register(r'rh', RhViewSet)

ator_router = routers.NestedSimpleRouter(router, r'pracas', lookup='praca')
ator_router.register(r'atores', AtorViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(imagem_router.urls)),
    url(r'^', include(parceiro_router.urls)),
    url(r'^', include(grupogestor_router.urls)),
    url(r'^', include(membrogestor_router.urls)),
    url(r'^', include(membrougl_router.urls)),
    url(r'^', include(rh_router.urls)),
    url(r'^', include(ator_router.urls)),
    url(r'^distancia/$', DistanceView.as_view(), name='distancia'),
]
