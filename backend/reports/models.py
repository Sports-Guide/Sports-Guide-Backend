from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Report(models.Model):
    REPORT_CHOICES = [
        ('WRONG_INFO', 'Неправильная информация'),
        ('CLOSED', 'Площадка закрылась'),
        ('CHANGE_COORDS', 'Уточнить местоположение'),
        ('OTHER', 'Другое'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    report_type = models.CharField(max_length=20, choices=REPORT_CHOICES)
    wrong_info = models.TextField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name='неправильная информация')
    images = models.ImageField(
        upload_to='area_images/',
        verbose_name='изображение'
    )
    latitude = models.DecimalField(
        max_digits=18,
        decimal_places=15,
        verbose_name='Широта',
        blank=True,
        null=True
    )
    longitude = models.DecimalField(
        max_digits=18,
        decimal_places=15,
        verbose_name='Долгота',
        blank=True,
        null=True
    )
    other_info = models.TextField(
        blank=True,
        null=True,
        max_length=256,
        verbose_name='другое'
    )

    class Meta:
        verbose_name = 'уточнение информации'
        verbose_name_plural = 'уточнение информации'
