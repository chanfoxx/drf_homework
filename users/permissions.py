from rest_framework.permissions import BasePermission


class IsUser(BasePermission):
    """ Права доступа для владельца. """
    message = 'Вы не являетесь владельцем страницы.'

    def has_object_permission(self, request, view, obj):
        """ Настраивает способ проверки разрешений. """
        return request.user == obj
