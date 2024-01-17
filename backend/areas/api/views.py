from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.response import Response

from areas.api.serializers import (AreaImageSerializer, AreaSerializer,
                                   CategorySerializer, CommentSerializer)
from areas.constants import ModerationStatus
from areas.models import Area, Category, Comment

from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class AreaViewSet(viewsets.ModelViewSet):
    serializer_class = AreaSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    parser_classes = (MultiPartParser, JSONParser)

    def get_queryset(self):
        match self.action:
            case 'list' | 'retrieve':
                return Area.objects.filter(
                    moderation_status=ModerationStatus.APPROVED.value
                )
            case 'add_images':
                return Area.objects.all()
            case _:
                return Area.objects.all()

    @action(detail=True, methods=['post'])
    def add_images(self, request, pk=None):
        area = self.get_object()
        images_data = request.FILES.getlist('image')
        response = []

        if not images_data:
            return Response({"detail": "Изображения не найдены."},
                            status=status.HTTP_400_BAD_REQUEST)

        for image_data in images_data:
            serializer = AreaImageSerializer(data={'image': image_data})
            if serializer.is_valid():
                serializer.save(area=area)
                response.append(serializer.data)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(response, status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
