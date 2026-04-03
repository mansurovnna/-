from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Имя пользователя",
        max_length=150,
        help_text="Обязательно. 150 символов или меньше. Только буквы, цифры и @/./+/-/_."
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput,
        help_text="Ваш пароль должен содержать не менее 8 символов и не быть слишком простым."
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput,
        help_text="Введите тот же пароль для подтверждения."
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Имя пользователя")
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput)