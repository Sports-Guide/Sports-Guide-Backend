import io
import os
import uuid

from PIL import Image
from django.core.files import File

from config.celery import app

from .models import Area, AreaImage


@app.task()
def process_area_images(area_id, file_paths):
    """
    Обрабатывает изображения для заданной площадки, сжимая их до FullHD
    разрешения и сохраняя с новым случайным именем в формате jpeg.
    """
    area = Area.objects.get(id=area_id)
    for file_path in file_paths:
        img = Image.open(file_path)
        img = img.convert('RGB')

        hd_size = (1920, 1080)
        img.thumbnail(hd_size, Image.Resampling.LANCZOS)

        random_filename = f'{area_id}-{uuid.uuid4()}.jpeg'

        temp_file = io.BytesIO()
        img.save(temp_file, format='JPEG', quality=50,
                 optimize=True, progressive=True)
        temp_file.seek(0)

        AreaImage.objects.create(area=area, image=File(temp_file,
                                                       name=random_filename))
        if os.path.exists(file_path):
            os.remove(file_path)
