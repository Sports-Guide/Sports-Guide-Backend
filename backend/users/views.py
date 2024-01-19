from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.response import Response

from .serializers import CustomUserCreateSerializer

User = get_user_model()


class CustomUserCreateViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = CustomUserCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = CustomUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
