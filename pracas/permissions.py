from rest_framework.compat import is_authenticated
from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS


class IsAdminOrManagerOrReadOnly(BasePermission):
    """
    Permite leitura de qualquer usuário e permite a atualização de informações
    por administradores MinC e a adição de novas instancias por administradores MinC.
    Exclusivo para administradores MinC.
    """

    def __init__(self):
        self.MANAGER_SAFE_METHODS = SAFE_METHODS + ('PUT', 'PATCH')
        self.ADMIN_FIELDS = ('contrato', 'repasse', 'modelo', 'lat', 'long')

    def has_permission(self, request, view):
        return (request.method in SAFE_METHODS or
                request.method in self.MANAGER_SAFE_METHODS and
                is_authenticated(request.user) or
                request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        elif bool(set(self.ADMIN_FIELDS).intersection(request.data)):
            return request.user.is_staff
        elif request.method in self.MANAGER_SAFE_METHODS:
            try:
                return request.user.is_staff or obj.get_manager().user == request.user
            except:
                return False
        else:
            return request.user.is_staff


class IsOwnerOrReadOnly(BasePermission):
    """
    Mesmas permissões que o IsAdminOrManagerOrReadOnly, porém mais permissivo 
    para englobar também o gestor da praça
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
