from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from users.models import User


class CustomUserCreationForm(UserCreationForm):
    """ Форма создания пользователя. """
    class Meta:
        model = User
        fields = ("email",)


class CustomUserChangeForm(UserChangeForm):
    """ Форма редактирования пользователя. """
    class Meta:
        model = User
        fields = ("email",)
