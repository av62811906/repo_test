from rest_framework.permissions import BasePermission


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type != 3:
            return False

        return True
