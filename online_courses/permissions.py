from rest_framework.permissions import BasePermission

from users.models import UserRole


class IsModerator(BasePermission):
    """ Права доступа для модератора. """
    message = 'Вы не являетесь модератором!'

    def has_permission(self, request, view):
        """ Настраивает способ проверки разрешений. """
        if request.user.role == UserRole.MODERATOR:
            return True
        return False


class IsOwner(BasePermission):
    """ Права доступа для владельца. """
    message = 'Вы не являетесь владельцем!'

    def has_object_permission(self, request, view, obj):
        """ Настраивает способ проверки разрешений. """
        return request.user == obj.owner
