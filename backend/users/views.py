from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import (
    CustomUserCreateSerializer,
    CustomUserSerializer,
    CustomUserShortSerializer,
)


class CustomUserViewSet(UserViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_serializer_class(self):
        match self.action:
            case 'list':
                return CustomUserShortSerializer
            case 'create':
                return CustomUserCreateSerializer
            case _:
                return CustomUserSerializer

    @action(methods=['post'], detail=False, url_path='me/upload_photo')
    def upload_photo(self, request, *args, **kwargs):
        user = request.user
        if 'photo' not in request.FILES:
            return Response({"detail": "Фото не найдено."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserSerializer(
            user, data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response({'photo': serializer.data.get('photo')},
                            status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
