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


class AreaSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())
    images = AreaImageSerializer(many=True, read_only=True)

    class Meta:
        model = Area
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = ('id', 'author', 'area', 'comment', 'date_added')
