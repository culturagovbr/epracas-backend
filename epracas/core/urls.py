from django.conf.urls import include, url

from .views import PracaViewSet

from rest_framework import routers 

router = routers.SimpleRouter()
router.register(r'pracas', PracaViewSet) 

urlpatterns = [
    url(r'^', include(router.urls)),
]
