from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from rest_framework.compat import is_authenticated

ADMIN_SAFE_METHODS = SAFE_METHODS + ('PUT', 'PATCH', 'DELETE')
MANAGER_SAFE_METHODS = ADMIN_SAFE_METHODS + ('POST', )

ADMIN_FIELDS = ('aprovado', 'valido', 'verificado')


class CommonUserOrReadOnly(BasePermission):
    """
    Permite criação apenas a usuários comuns, alteração e exclusão a usuários
    comuns e administradores.
    """

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.method in ADMIN_SAFE_METHODS and request.user.is_staff or
                request.method in MANAGER_SAFE_METHODS and
                is_authenticated(request.user) and not request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if bool(set(ADMIN_FIELDS).intersection(request.data)):
            return request.user.is_staff
        elif request.method in MANAGER_SAFE_METHODS:
            return obj.user == request.user or request.user.is_staff


class IsManagerOrReadOnly(BasePermission):
    """
    Permite leitura por qualquer usuário, mas administradores e gestores de
    Praça podem adicionar novas instancias.
    """

    def __init__(self):
        self.MANAGER_SAFE_METHODS = SAFE_METHODS + ('POST', 'PUT', 'PATCH', 'DELETE')

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.method in self.MANAGER_SAFE_METHODS and
                is_authenticated(request.user) or
                request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif request.method in self.MANAGER_SAFE_METHODS:
            try:
                return request.user.is_staff or obj.get_manager().user == request.user
            except:
                return False
        else:
            return request.user.is_staff
