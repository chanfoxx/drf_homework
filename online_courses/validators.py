from urllib.parse import urlparse

from rest_framework.serializers import ValidationError


class LessonsLinkValidator:
    """ Валидатор для поля - ссылка на видео. """
    def __init__(self, field):
        """
        Создание экземпляра класса LessonsLinkValidator.

        :param fields: Название поля для валидации.
        """
        self.field = field

    def __call__(self, attrs):
        """ Позволяет вызывать экземпляр класса как функцию. """
        value = attrs.get(self.field)
        parsed_link = urlparse(value)

        if parsed_link.netloc != "www.youtube.com":
            raise ValidationError('Видео должно быть с ресурса: youtube.com.')
