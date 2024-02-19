from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from areas.models import (
    Area,
    AreaImage,
    Category,
    Comment,
    Report,
    ReportImage,
)
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

    def create(self, validated_data):
        """
        Создает площадку, учитывая переданные категории и изображения.
        """
        category_ids = validated_data.pop('categories', [])
        images_data = validated_data.pop('images', [])
        area = super().create(validated_data)

        area.categories.set(category_ids)

        if images_data:
            for image_data in images_data:
                AreaImage.objects.create(area=area, image=image_data)
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
        images_serializer = AreaImageSerializer(
            instance.areaimage_set.all(), many=True
        )
        representation['images'] = images_serializer.data
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


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = ReportImage
        fields = ('image',)


class ReportSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)
    latitude = serializers.DecimalField(
        max_digits=18,
        decimal_places=15,
        required=False
    )
    longitude = serializers.DecimalField(
        max_digits=18,
        decimal_places=15,
        required=False
    )

    class Meta:
        model = Report
        fields = [
            'report_type',
            'description',
            'latitude',
            'longitude',
            'images'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        report = Report.objects.create(**validated_data)
        for image_data in images_data:
            ReportImage.objects.create(report=report, **image_data)
        return report
