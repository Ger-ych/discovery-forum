from rest_framework import permissions


# is owner permission
class IsOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if not hasattr(obj, 'user'):
            return False
        return obj.user == request.user
