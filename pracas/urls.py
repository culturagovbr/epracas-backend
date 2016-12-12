from django.conf.urls import include, url

from rest_framework import routers

from .views import PracaUploadHeader
from .views import PracaVinculoUpload
from .views import PracaViewSet
from .views import DistanceView

from .views import ParceiroViewSet


router = routers.SimpleRouter()

router.register(r'pracas', PracaViewSet)
router.register(r'parceiros', ParceiroViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^pracas/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/header_upload/$',
        PracaUploadHeader.as_view(),
        name='praca-header_upload'
        ),
    url(r'^pracas/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/vinculo_upload/$',
        PracaVinculoUpload.as_view(),
        name='praca-vinculo_upload'
        ),
    url(r'^distancia/$',
        DistanceView.as_view(),
        name='distancia'
        ),
]
