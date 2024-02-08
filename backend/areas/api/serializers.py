from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from areas.models import Area, AreaImage, Category, Comment
from users.api.serializers import (
    CustomUserSerializer,
    CustomUserShortSerializer,
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AreaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaImage
        fields = ('id', 'image')


class CommentSerializer(serializers.ModelSerializer):
    author = CustomUserShortSerializer(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'area', 'comment', 'date_added')


class AreaSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(
        default=serializers.CurrentUserDefault(),
    )
    images = AreaImageSerializer(
        many=True,
        read_only=True,
        source='areaimage_set'
    )

    class Meta:
        model = Area
        fields = ('id', 'address', 'description', 'author', 'latitude',
                  'longitude', 'categories', 'images',)


class AreaReadSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    author = CustomUserSerializer()
    categories = CategorySerializer(many=True)
    images = AreaImageSerializer(
        many=True,
        read_only=True,
        source='areaimage_set'
    )
    is_favorited = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Area
        fields = ('id', 'name', 'address', 'description', 'moderation_status',
                  'author', 'latitude', 'longitude', 'categories', 'images',
                  'is_favorited')

    @extend_schema_field(serializers.CharField)
    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.favorite.exists()

    @extend_schema_field(serializers.CharField)
    def get_name(self, obj):
        categories = obj.categories.all()
        if len(categories) == 1:
            return categories[0].area_name
        return 'Спортивная площадка'
