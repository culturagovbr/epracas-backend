from django.conf.urls import include, url

from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'agenda', AgendaViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
]
