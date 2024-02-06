from djoser.views import UserViewSet
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.api.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):

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
