from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

from rest_framework.compat import is_authenticated


class IsAdminOrManagerOrReadOnly(BasePermission):
    """
    Permite leitura de qualquer usuário e permite a atualização de informações
    por administradores e gestores de Praça e a adição de novas instancias por
    administradores.
    """

    def __init__(self):
        self.MANAGER_SAFE_METHODS = SAFE_METHODS + ('PUT', 'PATCH')

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
                return request.user.is_staff or obj.gestor.user == request.user
            except:
                return False
        else:
            return request.user.is_staff


class IsOwnerOrReadOnly(BasePermission):
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
            except AttributeError:
                return False
        else:
            return request.user.is_staff
