from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsProductOwnerOrSuperUser(BasePermission):
    message = "You are neither a product owner nor a superuser"
    def has_permission(self, request, view):
        self.message = "No Permission"
        return True

    def has_object_permission(self, request, view, obj):
        self.message = "You must either be a product owner or a super user"
        return bool(
            request.user and request.user.is_superuser or
            request.user and obj.user == request.user
        )


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )


