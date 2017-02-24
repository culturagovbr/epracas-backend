from django.conf.urls import include, url

from .views import UserView
from .views import UserListView


urlpatterns = [
    url(r'user/(?P<sub>[0-9]+)/$',
        UserView.as_view(),
        name='user-detail',
       ),
    url(r'user/$',
        UserListView.as_view(),
        name='user-list',
       ),
]
