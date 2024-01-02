from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated

from subscriptions.permissions import IsOwner
from subscriptions.models import Subscription
from subscriptions.serializers import SubSerializer


class SubCreateAPIView(CreateAPIView):
    """ Представление для установки подписки. """
    serializer_class = SubSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Устанавливает текущего пользователя и меняет статут подписки. """
        new_subscriber = serializer.save()
        new_subscriber.subscriber = self.request.user
        new_subscriber.is_subscribed = True
        new_subscriber.save()


class SubDestroyAPIView(DestroyAPIView):
    """ Представление для удаления подписки. """
    queryset = Subscription.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
