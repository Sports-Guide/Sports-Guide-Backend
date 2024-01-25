import io
import os
import random

from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
from django.core.files.base import ContentFile


def avatar_create(nickname):
    """Метод для создания изображения."""
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
    image_size = (200, 200)

    # Создание изображения с рандомным фоновым цветом
    new_img = Image.new('RGB', image_size, random_color)

    # Создание объекта ImageDraw для рисования на изображении
    draw = ImageDraw.Draw(new_img)

    # Задание размера шрифта и выбор шрифта
    font_size = 120
    font_path = os.path.join(
        settings.BASE_DIR,
        'static/fonts/COMIC.TTF',
    )
    font = ImageFont.truetype(font_path, font_size)
    text = nickname[0].upper()

    # Рисование текста
    draw.text((55, 10), text, font=font, fill='white')

    # Преобразование изображения в байты (можно использовать BytesIO)
    image_io = io.BytesIO()
    new_img.save(image_io, format='PNG')
    image_bytes = image_io.getvalue()

    content_file = ContentFile(image_bytes, name=f'{nickname}_avatar.png')
    return content_file
