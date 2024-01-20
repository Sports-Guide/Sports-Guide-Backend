import base64
import io
import os
import random

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont

User = get_user_model()


def avatar_create(user):
    """'Метод для создание изображения."""
    color_list = [
        (0, 215, 56),
        (0, 213, 175),
        (20, 120, 170),
        (137, 20, 255),
        (255, 20, 20),
        (255, 20, 132),
        (255, 147, 20),
    ]

    random_color = random.choice(color_list)
    # Задание размеров изображения
    image_size = (300, 300)

    # Создание изображения с рандомным фоновым цветом
    new_img = Image.new("RGB", image_size, random_color)

    # Создание объекта ImageDraw для рисования на изображении
    draw = ImageDraw.Draw(new_img)

    # Задание размера шрифта и выбор шрифта
    font_size = 120
    font_path = os.path.join(
        settings.BASE_DIR,
        "static/fonts/COMIC.TTF",
    )
    font = ImageFont.truetype(font_path, font_size)
    text = user.nickname[0].upper()

    # Определение координат для размещения текста в центре
    text_width, text_height = text_size(text, font)
    text_position = (
        (image_size[0] - text_width) // 2,
        (image_size[1] - text_height) // 2,
    )

    # Рисование текста
    draw.text((text_position[0], 65), text, font=font, fill="white")

    # Преобразование изображения в байты (можно использовать BytesIO)
    image_io = io.BytesIO()
    new_img.save(image_io, format="PNG")
    image_bytes = image_io.getvalue()

    # Преобразование байтов в строку base64
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    content_file = ContentFile(
        base64.b64decode(image_base64), name=f"{user.nickname}_avatar.png"
    )
    return content_file


def text_size(text, font):
    width = font.getmask(text).getbbox()[2]
    height = font.getmask(text).getbbox()[3]
    return (width, height)
