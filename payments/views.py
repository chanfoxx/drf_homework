from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from payments.models import Payment
from payments.serializers import (PaymentCreateSerializer, PaymentListSerializer,
                                  PaymentDetailSerializer)


class PaymentListAPIView(generics.ListAPIView):
    """ Контроллер для списка платежей. """
    serializer_class = PaymentListSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    # Фильтрация по курсу, уроку, способу оплаты.
    filterset_fields = ('paid_course', 'paid_lesson', 'payment_method',)
    # Сортировка по дате.
    ordering_fields = ('payday',)


class PaymentCreateAPIView(generics.CreateAPIView):
    """ Контроллер для создания платежа. """
    serializer_class = PaymentCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """ Присваивает текущего пользователя для платежа. """
        new_payment = serializer.save(user=self.request.user)
        new_payment.user = self.request.user
        new_payment.save()


class PaymentDetailAPIView(generics.RetrieveAPIView):
    """ Контроллер для вывода конкретного платежа. """
    serializer_class = PaymentDetailSerializer
    queryset = Payment.objects.all()
    permission_classes = [IsAuthenticated]
