from rest_framework.permissions import SAFE_METHODS, BasePermission

ALLOWED_METHODS = ('POST', 'PATCH', 'DELETE')


class BlockedAccess(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsOwnerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        method = request.method
        is_auth = request.user.is_authenticated
        return method in SAFE_METHODS or method in ALLOWED_METHODS and is_auth

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user
