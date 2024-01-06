from datetime import timedelta

from django.utils import timezone
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from online_courses.models import Lesson
from online_courses.paginators import OnlineCoursePaginator
from online_courses.permissions import IsModerator, IsOwner
from online_courses.serializers.lesson import LessonSerializer
from online_courses.tasks import send_update


class LessonCreateAPIView(generics.CreateAPIView):
    """ Представление для создания урока. """
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        """
        Создает урок, присваивает автора,
        а также отправляет уведомление об обновлении.
        """
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()

        course = new_lesson.course
        # Отправляем письмо с обновлениями, если прошло более 4 часов.
        if course.last_updated < timezone.now() - timedelta(hours=4):
            subscribers = course.subscription.filter(
                is_subscribed=True).values_list('subscriber', flat=True)

            for user_id in subscribers:
                send_update.delay(user_id, new_lesson.title)


class LessonListAPIView(generics.ListAPIView):
    """ Представление для вывода списка уроков. """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = OnlineCoursePaginator
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """ Представление для вывода определенного урока. """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """ Представление для изменения урока. """
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]

    def perform_create(self, serializer):
        """ Создает отправку обновлений пользователям. """
        update_lesson = serializer.save()
        course = update_lesson.course
        # Отправляем письмо с обновлениями, если прошло более 4 часов.
        if course.last_updated < timezone.now() - timedelta(hours=4):
            subscribers = course.subscription.filter(
                is_subscribed=True).values_list('subscriber', flat=True)

            for user_id in subscribers:
                send_update.delay(user_id, update_lesson.title)


class LessonDestroyAPIView(generics.DestroyAPIView):
    """ Представление для удаления урока. """
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
