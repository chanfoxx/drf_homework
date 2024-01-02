from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from online_courses.models import Lesson
from online_courses.paginators import OnlineCoursePaginator
from online_courses.permissions import IsModerator, IsOwner
from online_courses.serializers.lesson import LessonSerializer


class LessonCreateAPIView(generics.CreateAPIView):
    """Представление для создания урока."""
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonListAPIView(generics.ListAPIView):
    """Представление для вывода списка уроков."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = OnlineCoursePaginator
    permission_classes = [IsAuthenticated]


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Представление для вывода определенного урока."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Представление для изменения урока."""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Представление для удаления урока."""
    queryset = Lesson.objects.all()
    permission_classes = [IsAuthenticated, IsOwner]
