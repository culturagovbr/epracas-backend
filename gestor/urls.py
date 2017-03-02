from django.conf.urls import include, url

from rest_framework_nested import routers

from .views import GestorViewSet
from .views import ProcessoViewSet
from .views import ArquivoProcessoViewSet

router = routers.SimpleRouter()

router.register(r'gestor', GestorViewSet)
router.register(r'processo', ProcessoViewSet)

processo_router = routers.NestedSimpleRouter(
    router, r'processo', lookup='processo')
processo_router.register(
    r'documento',
    ArquivoProcessoViewSet,
    base_name='documento')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(processo_router.urls)),
]
