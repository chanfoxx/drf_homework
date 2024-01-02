from rest_framework import serializers

from subscriptions.models import Subscription


class SubSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели подписки на обновления. """
    class Meta:
        """ Метаданные для сериалайзера модели подписок на обновления. """
        model = Subscription
        fields = '__all__'
