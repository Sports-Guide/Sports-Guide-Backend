from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response

from users.models import CustomUser
from users.serializers import (
    CustomUserCreateSerializer,
    CustomUserSerializer,
    CustomUserPhotoSerializer,
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

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
    def upload_photo(self, request, id=None):
        user = self.get_object()
        photo_data = request.FILES.get('photo')
        response = []

        if not photo_data:
            return Response({"detail": "Фотография не найдена."},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = CustomUserPhotoSerializer(data={'photo': photo_data})
        if serializer.is_valid():
            user.photo.delete()
            user.photo.save(photo_data.name, photo_data, save=True)
            response.append(serializer.data)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_201_CREATED)
