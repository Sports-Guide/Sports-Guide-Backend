from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from areas.api.serializers import (
    AreaReadSerializer,
    AreaSerializer,
    CategorySerializer,
    CommentSerializer,
)
from areas.constants import ModerationStatus
from areas.models import Area, Category, Comment, FavoriteArea

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
    parser_classes = [MultiPartParser, JSONParser]

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
                ).select_related(
                    'author'
                ).prefetch_related(
                    'categories', 'areaimage_set', 'favorite'
                )
            case 'add_images':
                return Area.objects.all()
            case _:
                return Area.objects.all()

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
        serializer = AreaReadSerializer(areas,
                                        many=True,
                                        context={'request': request})
        return Response(serializer.data)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk=None):
        area = self.get_object()
        if request.method == 'POST':
            favorite, created = FavoriteArea.objects.get_or_create(
                user=request.user, area=area
            )
            if not created:
                return Response(
                    {'detail': 'Площадка уже добавлена в избранное!'},
                    status=status.HTTP_409_CONFLICT
                )
            serializer = AreaSerializer(area)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            get_object_or_404(
                FavoriteArea, user=request.user, area=area
            ).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def favorites(self, request):
        user = self.request.user
        areas = Area.objects.filter(
            favorite__user=user
        ).select_related(
            'author'
        ).prefetch_related(
            'categories', 'areaimage_set', 'favorite'
        )
        serializer = AreaReadSerializer(areas,
                                        many=True,
                                        context={'request': request})
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    pagination_class = CommentPaginator
