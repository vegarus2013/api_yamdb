from rest_framework import permissions


class AuthorModeratorAdminOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return any(
            obj.author == request.user,
            request.user.role in ('admin', 'moderator'),
            request.method in permissions.SAFE_METHODS
        )
