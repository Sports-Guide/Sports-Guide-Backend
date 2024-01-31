from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer, UserSerializer

from .utils import avatar_create

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


class CustomUserPhotoSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'photo')
