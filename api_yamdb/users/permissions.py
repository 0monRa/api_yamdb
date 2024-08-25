from rest_framework.permissions import BasePermission, SAFE_METHODS

from api_yamdb.constants import ROLE_ADMIN, ROLE_MODERATOR


class AnonymousPermission(BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class AuthenticatedPermission(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj == request.user


class AuthorPermission(AuthenticatedPermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class ModeratorPermission(AuthenticatedPermission):

    def has_object_permission(self, request, view, obj):
        return True


class AdministratorPermission(BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return (request.user.is_superuser
                or request.user.role == ROLE_ADMIN)


class CustomReviewCommentPermission(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        if request.user.is_superuser or request.user.role == ROLE_ADMIN:
            return True

        if request.user.role == ROLE_MODERATOR and request.method in [
            'PATCH', 'DELETE'
        ]:
            return True

        if obj.author == request.user:
            return True

        return False
