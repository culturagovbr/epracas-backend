from django.conf.urls import include, url

from rest_framework import routers

from .views import GestorViewSet
from .views import ProcessoViewSet

router = routers.SimpleRouter()

router.register(r'gestor', GestorViewSet)
router.register(r'processo', ProcessoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
