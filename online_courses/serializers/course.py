import stripe
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers

from online_courses.models import Course, Lesson
from online_courses.serializers.lesson import LessonTitleSerializer
from subscriptions.models import Subscription
from subscriptions.serializers import SubBooleanSerializer


class CourseSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели курса. """
    def create(self, validated_data):
        """ Создает продукт для API stripe. """
        course = Course.objects.create(**validated_data)
        # Создаем продукт по API stripe.
        product = stripe.Product.create(name=course.title)
        # Присваиваем название полю курса.
        course.stripe_product_name = product.name
        # Сохраняем.
        course.save()

        return course

    class Meta:
        """ Метаданные для сериализатора модели курса. """
        model = Course
        fields = '__all__'


class CourseListSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели списка курсов. """
    lesson_count = serializers.SerializerMethodField(read_only=True)

    def get_lesson_count(self, instance):
        """ Получает количество уроков курса. """
        return Lesson.objects.filter(course=instance).count()

    class Meta:
        """ Метаданные для сериализатора модели курса. """
        model = Course
        fields = ('title', 'lesson_count',)


class CourseDetailSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели курса в деталях. """
    lessons = serializers.SerializerMethodField(read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    @swagger_serializer_method(serializer_or_field=LessonTitleSerializer)
    def get_lessons(self, instance):
        """ Получает список уроков курса. """
        return [lesson.title
                for lesson in Lesson.objects.filter(course=instance)]

    @swagger_serializer_method(serializer_or_field=SubBooleanSerializer)
    def get_is_subscribed(self, instance):
        """ Получает статус подписки. """
        try:
            subscription = Subscription.objects.get(
                course=instance,
                subscriber=self.context['request'].user)
        except Exception:
            return False
        else:
            return subscription.is_subscribed

    class Meta:
        """ Метаданные для сериализатора модели курса. """
        model = Course
        fields = (
            'title', 'lessons', 'description', 'preview', 'is_subscribed',
        )
