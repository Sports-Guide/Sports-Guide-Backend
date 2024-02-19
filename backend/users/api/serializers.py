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
        'invalid_data': 'Неверный логин или пароль',
        'inactive_user': 'Пожалуйста, активируйте вашу учетную запись, '
                         'перейдя по ссылке в письме.',
        'invalid_email': 'Пользователь с таким адресом электронной почты '
                         'не найден.'
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
            raise ParseError(self.error_messages['invalid_email'])
        return super().validate(attrs)


class CustomSendEmailResetSerializer(SendEmailResetSerializer):
    """
    Сериализатор для отправки запроса на сброс пароля.
    """
    def validate_email(self, value):
        """
        Проверяет, существует ли пользователь с данным email, а также
        запрещает восстановления пароля неактивным пользователям.
        """
        path = self.context.get('request').path
        user = User.objects.filter(email=value)
        if not user.exists():
            raise ValidationError(
                'Пользователь с таким адресом электронной почты не найден.'
            )
        if path == '/api/users/reset_password/':
            if not user.first().is_active:
                raise ValidationError(
                    'Пожалуйста, активируйте вашу учетную запись, '
                    'перейдя по ссылке в письме.'
                )
        return value
