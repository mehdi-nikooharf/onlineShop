from rest_framework.permissions import BasePermission

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class IsProductOwnerOrReadOnly(BasePermission):
    message = "You are not product owner"
    def has_permission(self, request, view):
        self.message = "No Permission"
        return True

    def has_object_permission(self, request, view, obj):
        self.message = "You must be product owner"
        return obj.user == request.user


class IsAdminUserOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user and
            request.user.is_staff
        )
