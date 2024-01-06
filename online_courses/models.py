from django.conf import settings
from django.db import models
from django.utils import timezone

from users.models import NULLABLE


class Course(models.Model):
    """ Модель курса. """
    title = models.CharField(max_length=150,
                             verbose_name='Название курса')
    preview = models.ImageField(upload_to='images/courses/',
                                **NULLABLE,
                                verbose_name='Превью(изображение)')
    description = models.TextField(**NULLABLE,
                                   verbose_name='Описание')
    stripe_product_name = models.CharField(max_length=150,
                                           **NULLABLE)
    last_updated = models.DateTimeField(default=timezone.now,
                                        verbose_name='Время последнего обновления')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL,
                              verbose_name='Автор курса',
                              default=1,
                              **NULLABLE)

    def save(self, *args, **kwargs):
        """ Обновляет поле last_updated. """
        self.last_updated = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        """ Возвращает строковое представление о модели курса. """
        return f'{self.title}'

    class Meta:
        """ Метаданные для модели курса. """
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'


class Lesson(models.Model):
    """ Модель урока. """
    title = models.CharField(max_length=150,
                             verbose_name='Название урока')
    description = models.TextField(**NULLABLE,
                                   verbose_name='Описание')
    course = models.ForeignKey(Course,
                               on_delete=models.CASCADE,
                               verbose_name='Название курса')
    preview = models.ImageField(upload_to='images/lesson/',
                                **NULLABLE,
                                verbose_name='Превью(изображение)')
    video_link = models.URLField(max_length=200,
                                 **NULLABLE,
                                 verbose_name='Ссылка на видео')
    stripe_product_name = models.CharField(max_length=150,
                                           verbose_name='Название stripe продукта',
                                           **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.SET_NULL,
                              verbose_name='Автор урока',
                              default=1,
                              **NULLABLE)

    def __str__(self):
        """ Возвращает строковое представление о модели урока. """
        return f'{self.title} ({self.course})'

    class Meta:
        """ Метаданные для модели урока. """
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
