from rest_framework.permissions import BasePermission

from api_yamdb.constants import (
    ROLE_ADMIN,
)


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class AdminPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (
            request.user.is_superuser
            or request.user.role == ROLE_ADMIN
        )

    def has_object_permission(self, request, view, obj):
        return True
