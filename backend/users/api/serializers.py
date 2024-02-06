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
    class Meta:
        model = User
        fields = ('id', 'nickname', 'photo')


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'email', 'photo')


class CustomUserCreateSerializer(UserCreateSerializer):

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
    default_error_messages = {
        "invalid_data": "Неверный логин или пароль",
        "inactive_user": "Пожалуйста, активируйте вашу учетную запись, "
                         "перейдя по ссылке в письме."
    }

    def validate(self, attrs):
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
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise ValidationError(
                "Пользователь с таким адресом электронной почты не найден."
            )
        return value
