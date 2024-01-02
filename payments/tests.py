import stripe
from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from online_courses.models import Course, Lesson
from payments.models import Payment
from users.models import User


class PaymentTestCase(APITestCase):
    """ Класс тестирования модели платежа. """

    def setUp(self) -> None:
        """ Подготовка тестового окружения для тестирования. """
        self.owner = User.objects.create(
            email='test@sky.pro',
            password='123qwe456rty')

        self.client.force_authenticate(user=self.owner)

        self.course = Course.objects.create(
            title='test'
        )

        self.lesson = Lesson.objects.create(
            title='test',
            course=self.course,
            video_link='https://www.youtube.com/watch',
            stripe_product_name='test'
        )

    def test_create_payment(self):
        """ Тестирование создания платежа для курса/урока. """

        data = {
            'amount': 3232,
            'paid_lesson': 1,
            'payment_method': 'TRF'
        }

        response = self.client.post(
            reverse('payments:payment_create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertTrue(
            Payment.objects.all().exists()
        )
