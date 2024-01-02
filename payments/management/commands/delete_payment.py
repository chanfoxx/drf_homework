from django.core.management.base import BaseCommand

from payments.models import Payment


class Command(BaseCommand):
    """ Удаляет данные из таблицы платежей. """
    def handle(self, *args, **kwargs) -> None:
        try:
            Payment.objects.all().delete()
        except Exception as e:
            print(f'Не удалось удалить данные из таблицы платежей.'
                  f'Ошибка: {str(e)}.')
