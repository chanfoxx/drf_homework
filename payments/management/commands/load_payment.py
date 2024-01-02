from django.core.management.base import BaseCommand
from config.settings import PAY_FILE
import json
from payments.models import Payment


class Command(BaseCommand):
    """ Загружает данные из фикстур в таблицу платежей. """
    def handle(self, *args, **kwargs):
        with open(PAY_FILE, encoding='utf-8') as file:
            data = json.load(file)
            for payment in data:
                Payment.objects.create(
                    user_id=payment['user'],
                    paid_course_id=payment['paid_course'],
                    paid_lesson_id=payment['paid_lesson'],
                    amount=payment['amount'],
                    payment_method=payment['payment_method'],
                )
