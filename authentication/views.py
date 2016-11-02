from django.contrib.auth import get_user_model

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from core.views import DefaultMixin

from authentication.serializers import UserSerializer

from authentication.auth_methods import JWTUserAPIAuth


class UserViewSet(DefaultMixin, APIView):

    authentication_classes = (JWTUserAPIAuth,)
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        User = get_user_model()
        users_list = User.objects.all()
        response = UserSerializer(users_list, many=True).data

        return Response(response)

    def post(self, request):

        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    def patch(self, request, pk):
        User = get_user_model()
        manager = request.user

        if not manager.is_staff:
            raise PermissionDenied()

        user = User.objects.get(pk=pk)
        serializer = UserSerializer(
            user,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
