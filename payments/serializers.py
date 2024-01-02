from rest_framework import serializers

from online_courses.models import Course, Lesson
from payments.models import Payment
from payments.services import create_stripe_price, create_stripe_session


class PaymentListSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели платежа. """

    class Meta:
        """ Метаданные для сериалайзера модели платежа. """
        model = Payment
        fields = '__all__'


class PaymentUserSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели платежа в представлении пользователя. """

    class Meta:
        """ Метаданные для сериалайзера модели платежа. """
        model = Payment
        fields = ('payday', 'amount',)


class PaymentCreateSerializer(serializers.ModelSerializer):
    """ Сериалайзер для создания платежа. """
    session_url = serializers.SerializerMethodField(read_only=True)

    def get_session_url(self, instance):
        """ Получает ссылку для оплаты."""
        course_id = instance.paid_course_id
        lesson_id = instance.paid_lesson_id

        if course_id:
            course = Course.objects.get(id=course_id)
            course_product_name = course.stripe_product_name
            # Создаем stripe цену для продукта.
            course_price_id = create_stripe_price(
                course_product_name,
                instance.amount
            )
            # Создаем stripe сессию и возвращаем ссылку на оплату.
            session_url = create_stripe_session(course_price_id)

        if lesson_id:
            lesson = Lesson.objects.get(id=lesson_id)
            lesson_product_name = lesson.stripe_product_name
            # Создаем stripe цену для продукта.
            lesson_price_id = create_stripe_price(
                lesson_product_name,
                instance.amount
            )
            # Создаем stripe сессию и возвращаем ссылку на оплату.
            session_url = create_stripe_session(lesson_price_id)

        return session_url

    class Meta:
        """ Метаданные для сериалайзера модели платежа. """
        model = Payment
        fields = '__all__'


class PaymentDetailSerializer(serializers.ModelSerializer):
    """ Сериалайзер для модели конкретного платежа. """
    class Meta:
        """ Метаданные для сериалайзера модели платежа. """
        model = Payment
        fields = '__all__'
