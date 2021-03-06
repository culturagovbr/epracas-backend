from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.exceptions import PermissionDenied

from core.views import DefaultMixin

from authentication.serializers import UserSerializer

from authentication.auth_methods import JWTUserAPIAuth

User = get_user_model()


class UserListView(DefaultMixin, ListAPIView):

    authentication_classes = (JWTUserAPIAuth,)
    permission_classes = (IsAdminUser,)

    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(DefaultMixin, APIView):

    authentication_classes = (JWTUserAPIAuth,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, sub=None):
        try:
            user_data = [User.objects.get(sub=sub)]
            response = UserSerializer(user_data, many=True).data
            return Response(response)

        except User.DoesNotExist:
            raise NotFound

    def post(self, request, sub):

        if request.user.sub != int(sub):
            raise PermissionDenied()

        serializer = UserSerializer(
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)

    def delete(self, request, sub):

        if request.user.is_staff:
            user = get_object_or_404(User, sub=sub)
            user.delete()
            return Response(status=204)

        if not request.user:
            raise NotAuthenticated

        if not request.user.is_staff:
            raise PermissionDenied

    def patch(self, request, sub):
        manager = request.user

        if not manager.is_staff:
            if request.user.sub != int(sub) or "is_staff" in request.data:
                raise PermissionDenied
            elif "is_staff" in request.data and request.data["is_staff"]:
                raise PermissionDenied
            else:

                try:
                    user = User.objects.get(sub=sub)
                except User.DoesNotExist:
                    raise NotFound

                serializer = UserSerializer(
                    user,
                    data=request.data,
                    partial=True
                )

                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
        else:
            try:
                user = User.objects.get(sub=sub)
            except User.DoesNotExist:
                raise NotFound

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


