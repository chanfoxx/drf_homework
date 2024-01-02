from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """ Права доступа для владельца подписки. """
    message = 'Вы не являетесь подписчиком!'

    def has_object_permission(self, request, view, obj):
        """ Настраивает способ проверки разрешений. """
        return request.user == obj.subscriber
