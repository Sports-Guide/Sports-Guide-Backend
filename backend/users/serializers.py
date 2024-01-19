import base64
import io
import random

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from PIL import Image, ImageDraw
from rest_framework import serializers

User = get_user_model()


class Base64ImageField(serializers.ImageField):
    """
    Класс для сериализации изображений в формате base64.
    """

    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith("data:image"):
            format, imgstr = data.split(";base64,")
            ext = format.split("/")[-1]
            data = ContentFile(base64.b64decode(imgstr), name=f"temp.{ext}")
        return super().to_internal_value(data)


class CustomUserSerializer(UserSerializer):
    photo = Base64ImageField(required=False)

    class Meta:
        model = User
        fields = ("id", "nickname", "photo")


class CustomUserCreateSerializer(UserCreateSerializer):
    photo = Base64ImageField(required=False)

    class Meta(UserCreateSerializer.Meta):
        fields = UserCreateSerializer.Meta.fields + ("photo",)

    def create(self, validated_data):
        # Извлекаем поле photo из validated_data
        photo_data = validated_data.pop("photo", None)

        # Создаем пользователя без поля photo
        user = super().create(validated_data)

        # Если есть данные photo, устанавливаем их для пользователя
        if not photo_data:
            print("нет фото, надо сделать!")
            photo_data = self.avatar_create(user)

            # photo_data = self.avatar_create(nickname=user.nickname)
        user.photo = photo_data
        user.save()

        return user

    def avatar_create(self, user):
        # Генерация случайного цвета в формате RGB
        random_color = (
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255),
        )
        # Задание размеров изображения
        image_size = (500, 500)
        # Создание изображения с рандомным фоновым цветом
        new_img = Image.new("RGB", image_size, random_color)
        # Создание объекта ImageDraw для рисования на изображении
        draw = ImageDraw.Draw(new_img)
        # Определение координат овала (левый верхний угол, правый нижний угол)
        # oval_coords = [(100, 100), (400, 400)]
        oval_coords = [(0, 0), (500, 500)]
        # Рисование овала
        draw.ellipse(oval_coords, fill=random_color)
        # Отображение изображения (необязательно)
        # new_img.show()
        # Применение маски к изображению
        new_img = new_img.convert("RGBA")
        mask = Image.new("L", image_size, 0)
        mask_draw = ImageDraw.Draw(mask)
        mask_draw.ellipse(oval_coords, fill=255)
        new_img.putalpha(mask)

        # Преобразование изображения в байты (можно использовать BytesIO)
        image_io = io.BytesIO()
        new_img.save(image_io, format="PNG")
        image_bytes = image_io.getvalue()
        # print(image_bytes)

        # Преобразование байтов в строку base64
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # Создание объекта ContentFile из байтов и сохранение
        content_file = ContentFile(
            base64.b64decode(image_base64), name=f"{user.nickname}_avatar.png"
        )
        return content_file
