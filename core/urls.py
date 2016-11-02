from django.conf.urls import include, url

from .views import PracaViewSet, PracaUploadHeader, DistanceView
from .views import GestorViewSet
from .views import ProcessoViewSet
from .views import AgendaViewSet

from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'pracas', PracaViewSet)
router.register(r'gestor', GestorViewSet)
router.register(r'processo', ProcessoViewSet)
router.register(r'agenda', AgendaViewSet)

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'^distancia/$',
        DistanceView.as_view(),
        name='distancia'
        ),
    url(r'^pracas/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/header_upload/$',
        PracaUploadHeader.as_view(),
        name='praca-header_upload'
        ),
    # url(r'^pracas/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/vinculo_upload/$',
    #     PracaVinculoUpload.as_view(),
    #     name='praca-vinculo_upload'
    #     ),
]
