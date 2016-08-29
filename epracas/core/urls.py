from django.conf.urls import include, url

from .views import PracaViewSet, GestorViewSet, ProcessoViewSet

from rest_framework import routers 

router = routers.SimpleRouter()
router.register(r'pracas', PracaViewSet) 
router.register(r'gestor', GestorViewSet)
router.register(r'processo', ProcessoViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
