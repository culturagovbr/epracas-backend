from django.conf.urls import include, url

from rest_framework import routers

from .views import AgendaViewSet

router = routers.SimpleRouter()
router.register(r'atividades', AgendaViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
