from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='название')
    description = models.TextField(max_length=1000, verbose_name='описание')

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'


class Area(models.Model):
    MODERATION_STATUS_CHOICES = [
        ('rejected', 'Отклонено'),
        ('pending', 'На рассмотрении'),
        ('approved', 'Одобрено'),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='автор'
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        verbose_name='категории'
    )
    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name='Широта'
    )
    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6,
        verbose_name='Долгота'
    )
    moderation_status = models.CharField(
        max_length=10,
        choices=MODERATION_STATUS_CHOICES,
        default='pending',
        verbose_name='статус модерации'
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата добавления'
    )
    description = models.TextField(max_length=1000, verbose_name='описание')

    class Meta:
        verbose_name = 'площадка'
        verbose_name_plural = 'площадки'


class AreaImage(models.Model):
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name='площадка'
    )
    image = models.ImageField(
        upload_to='area_images/',
        verbose_name='изображение'
    )

    class Meta:
        verbose_name = 'фото площадки'
        verbose_name_plural = 'фото площадок'


class Comment(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='авто'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        verbose_name='площадка'
    )
    comment = models.TextField(verbose_name='комментарий')
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата добавления'
    )

    class Meta:
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'
