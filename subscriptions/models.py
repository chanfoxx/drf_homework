from django.db import models
from django.conf import settings

from online_courses.models import Course
from users.models import NULLABLE


class Subscription(models.Model):
    """ Модель подписки на обновления. """
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               verbose_name='Название курса',
                               related_name='subscription')
    subscriber = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.SET_NULL,
                                   verbose_name='Подписчик',
                                   default=1,
                                   related_name='subscriber',
                                   **NULLABLE)
    is_subscribed = models.BooleanField(default=False,
                                        verbose_name='Статус подписки',
                                        **NULLABLE)

    def __str__(self):
        """ Возвращает строковое представление о модели подписки. """
        return f'{self.subscriber} подписан на курс.'

    class Meta:
        """ Метаданные для модели подписок на курс. """
        verbose_name = 'Подписка на курс'
        verbose_name_plural = 'Подписки на курс'
