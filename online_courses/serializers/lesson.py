import stripe
from rest_framework import serializers
from django.conf import settings

from online_courses.models import Lesson
from online_courses.validators import LessonsLinkValidator


stripe.api_key = settings.STRIPE_API_KEY


class LessonSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели урока. """
    def create(self, validated_data):
        """ Создает продукт для API stripe. """
        lesson = Lesson.objects.create(**validated_data)
        # Создаем продукт по API stripe.
        product = stripe.Product.create(name=lesson.title)
        # Присваиваем название полю курса.
        lesson.stripe_product_name = product.name
        # Сохраняем.
        lesson.save()

        return lesson

    class Meta:
        """ Метаданные для сериализатора модели урока. """
        model = Lesson
        fields = '__all__'
        validators = [LessonsLinkValidator(field='video_link')]


class LessonTitleSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели урока. """

    class Meta:
        """ Метаданные для сериализатора модели урока. """
        model = Lesson
        fields = ('title',)