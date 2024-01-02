from django.contrib.auth.models import AbstractUser
from django.db import models
from users.managers import UserManager


NULLABLE = {'blank': True, 'null': True}


class UserRole(models.TextChoices):
    """ Класс ролей для пользователя. """
    MODERATOR = 'MD', 'Модератор'
    MEMBER = 'MR', 'Пользователь'
    SUPER_USER = 'SP', 'Cупер-пользователь'


class User(AbstractUser):
    """ Модель пользователя. """
    username = None

    email = models.EmailField(unique=True, verbose_name='E-mail')
    role = models.CharField(max_length=2,
                            choices=UserRole.choices,
                            verbose_name='Статус пользователя',
                            default=UserRole.MEMBER)
    phone = models.CharField(max_length=35,
                             **NULLABLE,
                             verbose_name='Номер телефона')
    city = models.CharField(max_length=150,
                            **NULLABLE,
                            verbose_name='Город')
    avatar = models.ImageField(upload_to='images/users/',
                               **NULLABLE,
                               verbose_name='Аватарка')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """ Возвращает строковое представление о модели пользователя. """
        return f'{self.email}'

    class Meta:
        """ Метаданные для модели пользователя. """
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
