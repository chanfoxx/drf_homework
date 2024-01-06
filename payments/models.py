from django.db import models
from django.conf import settings

from users.models import NULLABLE


class Payment(models.Model):
    """ Модель платежа. """
    CASH = "CSH"
    TRANSFER = "TRF"

    PAYMENT_METHOD_CHOICES = (
        (CASH, "Cash"),
        (TRANSFER, "Transfer to account"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             verbose_name='Пользователь',
                             related_name='payments',
                             default=1)
    payday = models.DateTimeField(auto_now_add=True,
                                  verbose_name='Дата оплаты')
    paid_course = models.ForeignKey('online_courses.Course',
                                    on_delete=models.SET_NULL,
                                    **NULLABLE,
                                    verbose_name='Оплаченный курс')
    paid_lesson = models.ForeignKey('online_courses.Lesson',
                                    on_delete=models.SET_NULL,
                                    **NULLABLE,
                                    verbose_name='Оплаченный урок')
    amount = models.IntegerField(verbose_name='Cумма оплаты')
    payment_method = models.CharField(max_length=3,
                                      choices=PAYMENT_METHOD_CHOICES,
                                      default=TRANSFER,
                                      verbose_name='Способ оплаты')

    def __str__(self):
        """ Возвращает строковое представление о модели платежа. """
        return f'Дата оплаты: {self.payday}.\nСтоимость: {self.amount}.'

    class Meta:
        """ Метаданные для модели платежа. """
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ('-payday',)

        constraints = [
            models.CheckConstraint(check=models.Q(paid_course__isnull=True) | models.Q(paid_lesson__isnull=True),
                                   name='payment_constraint')
        ]
