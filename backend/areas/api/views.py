from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from areas.api.serializers import (
    AreaImageSerializer,
    AreaReadSerializer,
    AreaSerializer,
    CategorySerializer,
    CommentSerializer,
)
from areas.constants import ModerationStatus
from areas.models import Area, Category, Comment

from .filters import AreaFilter
from .pagination import CommentPaginator
from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class AreaViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('categories__slug',)
    filterset_class = AreaFilter

    def get_serializer_class(self):
        match self.action:
            case 'list' | 'retrieve':
                return AreaReadSerializer
            case _:
                return AreaSerializer

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

    @extend_schema(
        responses={
            201: inline_serializer(
                name='ImageResponse',
                fields={
                    'id': serializers.IntegerField(),
                    'image': serializers.CharField()
                }
            )
        }
    )
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser])
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

    @action(detail=True, methods=['get'])
    def comments(self, request, pk=None):
        area = self.get_object()
        comments = area.comments.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def my(self, request, pk=None):
        user = self.request.user
        areas = user.areas.all()
        serializer = AreaReadSerializer(areas, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = CommentPaginator
