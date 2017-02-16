from django.conf.urls import include, url

from rest_framework_nested import routers

from .views import AgendaViewSet
from .views import RelatorioViewSet

router = routers.SimpleRouter()
router.register(r'atividades', AgendaViewSet)

atividades_router = routers.NestedSimpleRouter(router, r'atividades', lookup='agenda')
atividades_router.register(r'relatorios', RelatorioViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^', include(atividades_router.urls)),
]
