from django.conf.urls import include, url

from .views import PracaListView

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'pracas', PracaListView)

urlpatterns = [
    url(r'^', include(router.urls)),
]
