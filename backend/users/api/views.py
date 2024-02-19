from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.api.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """
    ViewSet для пользователей.
    """

    def resend_activation(self, request, *args, **kwargs):
        super().resend_activation(request, *args, **kwargs)

        return Response({"email": request.data['email']})

    def destroy(self, request, *args, **kwargs):
        """
        Удаляет аккаунт текущего пользователя.
        """
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses={
            201: inline_serializer(
                name='PhotoResponse',
                fields={
                    'photo': serializers.CharField()
                }
            )
        }
    )
    @action(methods=['post'], detail=False, url_path='me/upload_photo')
    def upload_photo(self, request, *args, **kwargs):
        """
        Загружает и сохраняет фотографию пользователя.
        """
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
