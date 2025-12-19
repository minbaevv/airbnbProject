import permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS


class GuestPermissions(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == 'guest'
        )



class HostPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        return (
            request.user.is_authenticated
            and request.user.role == 'host'
        )
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user

class IsHost(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.property.owner == request.user

