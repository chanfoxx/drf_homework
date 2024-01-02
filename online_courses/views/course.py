from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from online_courses.models import Course
from online_courses.paginators import OnlineCoursePaginator
from online_courses.permissions import IsModerator, IsOwner
from online_courses.serializers.course import (CourseSerializer,
                                               CourseListSerializer,
                                               CourseDetailSerializer)


class CourseViewSet(viewsets.ModelViewSet):
    """Вьюсет CRUD для модели курса."""
    queryset = Course.objects.all()
    pagination_class = OnlineCoursePaginator
    default_serializer = CourseSerializer
    serializers = {
        'list': CourseListSerializer,
        'retrieve': CourseDetailSerializer,
    }

    def get_serializer_class(self):
        """Возвращает сериализатор в зависимости от выбора запроса."""
        return self.serializers.get(self.action, self.default_serializer)

    def get_permissions(self):
        """Возвращает права в зависимости от статуса пользователя."""
        if self.action == 'destroy':
            permission_classes = [IsAuthenticated, IsOwner]
        elif self.action == 'list' or self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'update' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated, IsModerator | IsOwner]

        return [permission() for permission in permission_classes]
