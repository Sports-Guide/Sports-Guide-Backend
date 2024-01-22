import base64

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from .utils import avatar_create

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """
    Класс для сериализации изображений в формате base64.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')
        return super().to_internal_value(data)


class CustomUserSerializer(UserSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ('id', 'nickname', 'photo')


class CustomUserCreateSerializer(UserCreateSerializer):
    photo = Base64ImageField(required=False)

    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields + ('photo',)

    def create(self, validated_data):
        photo_data = validated_data.pop('photo', None)
        user = super().create(validated_data)
        if not photo_data:
            photo_data = avatar_create(user)
        user.photo = photo_data
        user.save()
        return user
