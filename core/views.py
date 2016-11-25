from rest_framework import filters
from rest_framework.viewsets import ModelViewSet


class DefaultMixin(object):
    filter_backends = (
            filters.DjangoFilterBackend,
            filters.SearchFilter,
            )


class MultiSerializerViewSet(ModelViewSet):

    def get_serializer_class(self):
        if self.action in self.serializers:
            return self.serializers.get(
                    self.action,
                    self.serializers[self.action]
                    )
        else:
            return self.serializer_class
