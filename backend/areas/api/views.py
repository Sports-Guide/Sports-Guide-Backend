from rest_framework import viewsets

from areas.api.serializers import (AreaSerializer, CategorySerializer,
                                   CommentSerializer)
from areas.models import Area, Category, Comment

from .permissions import IsAdminOrReadOnly, IsAuthorOrAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)


class AreaViewSet(viewsets.ModelViewSet):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
