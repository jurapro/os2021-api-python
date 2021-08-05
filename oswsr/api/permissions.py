from rest_framework import permissions, status
from rest_framework.authentication import get_authorization_header

from .exceptions import CafeAPIException
from .models import User


class IsAuthenticated(permissions.BasePermission):

    def has_permission(self, request, view):
        user = User.get_auth_user(request=request)
        if not user:
            raise CafeAPIException(message='Login failed',
                                   code=status.HTTP_403_FORBIDDEN)
        return True


class IsAdmin(IsAuthenticated):

    def has_permission(self, request, view):
        super().has_permission(request, view)
        user = User.get_auth_user(request=request)
        if user.role.code != 'admin':
            raise CafeAPIException(message='Forbidden for you”',
                                   code=status.HTTP_403_FORBIDDEN)
        return True
