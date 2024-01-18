from rest_framework import serializers

from payments.serializers import PaymentUserSerializer

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели пользователя. """

    class Meta:
        """ Метаданные для сериализатора модели пользователя. """
        model = User
        fields = ('email', 'password', 'phone', 'city', 'avatar',)


class UserDetailSerializer(serializers.ModelSerializer):
    """ Сериализатор для деталей модели пользователя. """
    payments = PaymentUserSerializer(many=True, read_only=True)

    class Meta:
        """ Метаданные для сериализатора модели пользователя. """
        model = User
        fields = ('email', 'password', 'first_name', 'last_name', 'avatar',
                  'phone', 'city', 'payments')


class OtherDetailSerializer(serializers.ModelSerializer):
    """ Сериализатор для просмотра чужих моделей пользователя. """

    class Meta:
        """ Метаданные для сериализатора модели пользователя. """
        model = User
        fields = ('email', 'first_name', 'avatar', 'phone', 'city',)
