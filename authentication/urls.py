from django.conf.urls import include, url

from .views import UserViewSet


urlpatterns = [
    url(r'user/(?P<pk>[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12})/$',
        UserViewSet.as_view(),
       ),
    url(r'user/$',
        UserViewSet.as_view(),
        name='user-list',
       ),
]
