from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from users.models import User


@shared_task
def block_inactive_user():
    """
    Проверяет активность пользователей;
    если пользователь не заходил больше 30 дней,
    автоматически меняется статус is_active.
    """
    time_difference = timezone.now() - timedelta(days=30)
    inactive_users = User.objects.filter(last_login__lt=time_difference)

    for user in inactive_users:
        user.is_active = False
        user.save()
