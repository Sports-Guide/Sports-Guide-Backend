from rest_framework import serializers

from areas.models import Area, AreaImage, Category, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class AreaImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaImage
        fields = ('id', 'image')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'author', 'area', 'comment', 'date_added')


class AreaSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images = AreaImageSerializer(
        many=True,
        read_only=True,
        source='areaimage_set'
    )

    class Meta:
        model = Area
        fields = ('id', 'author', 'latitude',
                  'longitude', 'categories', 'images',)
