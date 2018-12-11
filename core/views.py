from rest_framework import filters
from rest_framework.viewsets import ModelViewSet

from django_filters.rest_framework import DjangoFilterBackend
# from django_filters.rest_framework import filters


class DefaultMixin(object):
    filter_backends = (
        DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)


class MultiSerializerViewSet(ModelViewSet):
    def get_serializer_class(self):
        if self.action in self.serializers:
            return self.serializers.get(self.action,
                                        self.serializers[self.action])
        else:
            return self.serializer_class
