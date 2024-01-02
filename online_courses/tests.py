from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from online_courses.models import Course, Lesson
from users.models import User


class LessonsTestCase(APITestCase):
    """ Класс тестирования модели уроков. """

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
            video_link='https://www.youtube.com/watch'
        )

    def test_create_lesson(self):
        """ Тестирование создания урока для курса. """

        data = {
            'title': 'test2',
            'course': self.course.id,
            'video_link': 'https://www.youtube.com/'
        }

        response = self.client.post(
            reverse('online_courses:lesson-create'),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            2
        )

    def test_get_lessons_list(self):
        """ Тестирование вывода списка уроков. """

        response = self.client.get(
            reverse('online_courses:lessons-list')
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    {
                        "id": 1,
                        "title": "test",
                        "description": None,
                        "preview": None,
                        "video_link": "https://www.youtube.com/watch",
                        "course": 1,
                        "owner": 1
                    }
                ]
            }
        )

    def test_get_lesson(self):
        """ Тестирование вывода одного урока. """
        pk = self.lesson.pk
        response = self.client.get(
            reverse('online_courses:lesson', args=[pk])
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "title": "test",
                "description": None,
                "preview": None,
                "video_link": "https://www.youtube.com/watch",
                "course": 1,
                "owner": 1
            }
        )

    def test_update_lesson(self):
        """ Тестирование редактирования урока для курса. """

        data = {
            "video_link": "https://www.youtube.com/watch/video"
        }

        response = self.client.patch(
            reverse('online_courses:lesson-update', args=[self.lesson.pk]),
            data=data
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "title": "test",
                "description": None,
                "preview": None,
                "video_link": "https://www.youtube.com/watch/video",
                "course": 1,
                "owner": 1
            }
        )

    def test_delete_lesson(self):
        """ Тестирование удаления урока. """

        response = self.client.delete(
            reverse('online_courses:lesson-delete', args=[self.lesson.pk]),
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.assertEqual(
            Lesson.objects.all().count(),
            0
        )
