from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from online_courses.models import Course
from subscriptions.models import Subscription
from users.models import User


class SubTestCase(APITestCase):
    """ Класс тестирования модели подписки на курс. """

    def setUp(self) -> None:
        """ Подготовка тестового окружения для тестирования. """
        self.owner = User.objects.create(
            email='test@sky.pro',
            password='123qwe456rty')

        self.client.force_authenticate(user=self.owner)

        self.course = Course.objects.create(
            title='test'
        )

        self.subscription = Subscription.objects.create(
            course=self.course,
            subscriber=self.owner
        )

    def test_create_subscription(self):
        """ Тестирование создания подписки на курс. """

        data = {
            'course': self.course.id,
            'subscriber': self.owner.id
        }

        response = self.client.post(
            reverse('subscriptions:sub-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Subscription.objects.all().count(),
            2
        )

    def test_delete_subscription(self):
        """ Тестирование удаления подписки на курс. """
        response = self.client.delete(
            reverse('subscriptions:sub-delete', args=[self.subscription.pk]),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Subscription.objects.all().count(),
            0
        )
