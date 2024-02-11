from django.conf import settings
from django.contrib.auth import get_user_model
from djoser.serializers import (
    SendEmailResetSerializer,
    UserCreateSerializer,
    UserSerializer,
)
from rest_framework.exceptions import (
    AuthenticationFailed,
    ParseError,
    ValidationError,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.utils import avatar_create

User = get_user_model()


class CustomUserShortSerializer(UserSerializer):
    """
    Краткий сериализатор для пользовательских данных.
    """
    class Meta:
        model = User
        fields = ('id', 'nickname', 'photo')


class CustomUserSerializer(UserSerializer):
    """
    Расширенный сериализатор для пользовательских данных.
    """
    class Meta:
        model = User
        fields = ('id', 'nickname', 'email', 'photo')
        read_only_fields = ('email',)


class CustomUserCreateSerializer(UserCreateSerializer):
    """
    Сериализатор для создания новых пользователей.
    """
    def save(self, **kwargs):
        user = super().save(**kwargs)

        if not user.photo:
            avatar_file = avatar_create(user.nickname)
            user.photo.save(
                f'{user.nickname}_avatar.png',
                avatar_file,
                save=True
            )
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Сериализатор для получения пары токенов доступа и обновления.

    Расширяет стандартный сериализатор, добавляя кастомные сообщения об
    ошибках.
    Обрабатывает случаи неверных данных аутентификации и
    неактивных пользовательских аккаунтов.
    """
    default_error_messages = {
        "invalid_data": "Неверный логин или пароль",
        "inactive_user": "Пожалуйста, активируйте вашу учетную запись, "
                         "перейдя по ссылке в письме."
    }

    def validate(self, attrs):
        """
        Валидирует данные пользователя и генерирует токены доступа,
        обрабатывая ошибки аутентификации.
        """
        try:
            user = User.objects.get(email=attrs.get('email'))
            if not user.check_password(attrs.get('password')):
                raise ParseError(self.error_messages['invalid_data'])
            if not user.is_active:
                raise AuthenticationFailed(
                    self.error_messages['inactive_user']
                )
        except User.DoesNotExist:
            raise ParseError(self.error_messages['invalid_data'])
        return super().validate(attrs)


class CustomSendEmailResetSerializer(SendEmailResetSerializer):
    """
    Сериализатор для отправки запроса на сброс пароля.
    """
    def get_user(self, is_active=True):
        """
        Возвращает пользователя по email.

        Расширяет стандартный метод, позволяя неактивным пользователям
        сбросить пароль.
        """
        try:
            user = User.objects.get(
                **{self.email_field: self.data.get(self.email_field, "")},
            )
            if user.has_usable_password():
                return user
        except User.DoesNotExist:
            pass
        if (settings.PASSWORD_RESET_SHOW_EMAIL_NOT_FOUND
                or settings.USERNAME_RESET_SHOW_EMAIL_NOT_FOUND):
            self.fail("email_not_found")

    def validate_email(self, value):
        """
        Проверяет, существует ли пользователь с данным email.
        """
        if not User.objects.filter(email=value).exists():
            raise ValidationError(
                "Пользователь с таким адресом электронной почты не найден."
            )
        return value
