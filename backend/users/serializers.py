import base64
import io
import os
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from djoser.serializers import UserCreateSerializer, UserSerializer
from PIL import Image, ImageDraw, ImageFont
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

        if not photo_data:
            photo_data = self.avatar_create(user)
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

        # Задание размера шрифта и выбор шрифта
        font_size = 100
        # font = ImageFont.load_default()
        # font_path = settings.STATIC_URL + "fonts/ComicScansMS3.ttf"
        font_path = os.path.join(
            settings.BASE_DIR,
            # "static/fonts/ComicSansMS3.ttf",
            "static/fonts/COMIC.TTF",
        )
        font = ImageFont.truetype(font_path, font_size)

        # Определение координат для размещения текста
        text_position = (200, 200)
        text = user.nickname[0].upper()  # Получение первой буквы никнейма

        # Определение координат овала (левый верхний угол, правый нижний угол)
        oval_coords = [(0, 0), (500, 500)]

        # Рисование овала
        draw.ellipse(oval_coords, fill=random_color)

        # Рисование текста
        draw.text(text_position, text, font=font, fill="white")

        # Преобразование изображения в байты (можно использовать BytesIO)
        image_io = io.BytesIO()
        new_img.save(image_io, format="PNG")
        image_bytes = image_io.getvalue()

        # Преобразование байтов в строку base64
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        # Создание объекта ContentFile из байтов и сохранение
        content_file = ContentFile(
            base64.b64decode(image_base64), name=f"{user.nickname}_avatar.png"
        )
        return content_file
