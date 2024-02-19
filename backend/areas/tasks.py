import io
import os
import uuid

from PIL import Image
from django.core.files import File
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from config.celery import app
from core.constants import FROM_EMAIL

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


@app.task()
def send_moderation_email(user_email, status):
    ru_status = {'approved': 'одобрено', 'rejected': 'отклонено'}

    subject = 'Статус модерации для Вашей площадки изменен'
    context = {'moderation_status': ru_status[status]}
    html_message = render_to_string('core/email/area_moderation.html', context)
    email = EmailMessage(
        subject,
        html_message,
        FROM_EMAIL,
        [user_email],
    )
    email.content_subtype = 'html'
    email.send()
