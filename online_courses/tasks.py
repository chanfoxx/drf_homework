from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

from users.models import User


@shared_task
def send_update(user_id, lesson_title):
    """ Отправляет письмо с обновлениями курса подписчикам. """
    user = User.objects.get(pk=user_id)
    message = (f'В курсе, на который Вы подписаны, '
               f'появился новый урок: {lesson_title}.\n'
               f'Скорее посмотрите.')

    try:
        # Пробуем отправить сообщение.
        send_mail(
            subject='Уведомление об обновлении курса',
            message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )
    except Exception as e:
        return f"Ошибка отправки сообщения - {str(e)}."
    else:
        return "Сообщение отправлено."
