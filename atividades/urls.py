from django.conf.urls import include, url

from rest_framework_nested import routers

from .views import AgendaViewSet
from .views import RelatorioViewSet
from .views import RelatorioImagensViewSet

from .views import AreaViewSet

router = routers.SimpleRouter()
router.register(r'atividades', AgendaViewSet)
router.register(r'areas', AreaViewSet)

atividades_router = routers.NestedSimpleRouter(router, r'atividades', lookup='agenda')
atividades_router.register(r'relatorios', RelatorioViewSet, base_name='relatorio')

relatorio_router = routers.NestedSimpleRouter(atividades_router, r'relatorios', lookup='relatorio')
relatorio_router.register(r'imagens', RelatorioImagensViewSet, base_name='relatorio_imagem')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(atividades_router.urls)),
    url(r'^', include(relatorio_router.urls)),
]


