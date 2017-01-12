#coding: utf-8

from django.contrib.auth import get_user_model

from oidc_auth.authentication import JSONWebTokenAuthentication


class JWTUserAPIAuth(JSONWebTokenAuthentication):
    """
    Autenticação baseada em JWT que cria um novo usuário no backend
    quando do primeiro acesso e atualiza suas informações a cada
    novo acesso.
    """

    www_authenticate_realm = 'api'

    def get_user_by_id(self, request, id_token):
        User = get_user_model()
        user, created = User.objects.get_or_create(sub=id_token.get('sub'))
        return user

    def authenticate(self, request):
        jwt_value = self.get_jwt_value(request)
        if jwt_value is None:
            return None

        payload = self.decode_jwt(jwt_value)
        self.validate_claims(payload)

        user = self.get_user_by_id(request, payload)

        return user, payload
