from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer

from .fields import Base64ImageField

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    photo = Base64ImageField(required=True)

    class Meta:
        model = User
        fields = ("id", "nickname", "photo")
