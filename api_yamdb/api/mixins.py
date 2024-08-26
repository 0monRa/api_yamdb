from users.permissions import AnonymousPermission


class PermissionsMixin:

    def get_permissions(self):
        if self.action in {'list', 'retrieve'}:
            return (AnonymousPermission(),)
        return super().get_permissions()
