import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from areas.models import Area, AreaImage, Category, Comment
from areas.tasks import process_area_images
from core.constants import MAX_IMAGE_SIZE
from users.api.serializers import (
    CustomUserSerializer,
    CustomUserShortSerializer,
)


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели категорий.
    """
    class Meta:
        model = Category
        fields = '__all__'


class AreaImageSerializer(serializers.ModelSerializer):
    """
    Сериализатор для изображений площадок.
    """
    class Meta:
        model = AreaImage
        fields = ('image',)


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для комментариев.
    """
    author = CustomUserShortSerializer(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'author', 'area', 'comment', 'date_added')


class AreaSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания и обновления площадок.
    """
    author = CustomUserSerializer(
        default=serializers.CurrentUserDefault(),
    )
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )
    categories = serializers.CharField(required=True)

    class Meta:
        model = Area
        fields = ('id', 'address', 'description', 'author', 'latitude',
                  'longitude', 'categories', 'images',)

    def validate_categories(self, value):
        """
        Валидирует категории, убеждаясь, что указаны существующие ID категорий.
        """
        try:
            category_ids = [int(id.strip()) for id in value.split(',')]
        except ValueError:
            raise serializers.ValidationError(
                'Категории должны быть перечислены через запятую '
                'как целые числа.'
            )

        if not Category.objects.filter(id__in=category_ids).count() == len(
                category_ids):
            raise serializers.ValidationError(
                'Одна или несколько категорий не существуют.'
            )
        return category_ids

    def validate_images(self, value):
        """
        Валидирует изображения, проверяя их количество и размер.
        """
        if len(value) > 4:
            raise serializers.ValidationError(
                'Нельзя загрузить больше 4 изображений.'
            )

        for img in value:
            if img.size > MAX_IMAGE_SIZE:
                raise serializers.ValidationError(
                    'Размер изображения не должен превышать 5MB.'
                )
        return value

    def create(self, validated_data):
        """
        Создает площадку, учитывая переданные категории и изображения.
        """
        category_ids = validated_data.pop('categories', [])
        images_data = validated_data.pop('images', [])
        area = super().create(validated_data)

        area.categories.set(category_ids)

        if images_data:
            file_paths = []
            for image in images_data:
                temp_storage = FileSystemStorage(
                    location=os.path.join(settings.MEDIA_ROOT, 'temp')
                )
                filename = temp_storage.save(f"{area.id}_{image.name}", image)
                file_path = temp_storage.path(filename)
                file_paths.append(file_path)

            process_area_images.delay(area.id, file_paths)

        return area

    def to_representation(self, instance):
        """
        Представляет площадку, включая данные о категориях и изображениях.
        """
        representation = super().to_representation(instance)
        categories_serializer = CategorySerializer(
            instance.categories.all(), many=True
        )
        representation['categories'] = categories_serializer.data
        return representation


class AreaReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для чтения площадок.
    """
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
        """
        Определяет, добавлена ли площадка в избранное текущим пользователем.
        """
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return obj.favorite.exists()

    @extend_schema_field(serializers.CharField)
    def get_name(self, obj):
        """
        Генерирует название для площадки на основе категорий.
        """
        categories = obj.categories.all()
        if len(categories) == 1:
            return categories[0].area_name
        return 'Спортивная площадка'
