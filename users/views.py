from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import User
from users.permissions import IsUser
from users.serializers import UserSerializer, UserDetailSerializer, OtherDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    """ Сет представлений для модели пользователя. """
    queryset = User.objects.all()
    default_serializer = UserSerializer
    serializers = {
        'owner': UserDetailSerializer,
        'other': OtherDetailSerializer,
    }

    def get_object(self):
        """ Получает пользователя. """
        return self.request.user

    def perform_create(self, serializer):
        """ Переопределяет и сохраняет пароль. """
        user = serializer.save()
        user.set_password(user.password)
        user.save()

    def get_serializer_class(self):
        """ Возвращает сериализатор в зависимости от выбора запроса. """
        if self.action == "retrieve":
            if self.request.user == self.get_object():
                return self.serializers.get('owner')
            else:
                return self.serializers.get('other')
        else:
            return self.default_serializer

    def get_permissions(self):
        """ Возвращает права в зависимости от статуса пользователя. """
        if self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsUser]
        else:
            permission_classes = [AllowAny]

        return [permission() for permission in permission_classes]
