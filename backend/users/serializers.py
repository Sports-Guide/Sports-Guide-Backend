from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer

User = get_user_model()


class CustomUserShortSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'photo')


class CustomUserSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'nickname', 'email', 'photo')
