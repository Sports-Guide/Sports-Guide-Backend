from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from areas.validators import validate_category_name

User = get_user_model()


class Category(models.Model):
    name = models.CharField(
        unique=True,
        max_length=30,
        validators=[MinLengthValidator(3), validate_category_name],
        verbose_name='название'
    )
    area_name = models.CharField(
        max_length=50,
        verbose_name='название площадки'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        verbose_name='уникальный тег',
    )

    def __str__(self):
        return self.name

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
        related_name='areas',
        verbose_name='автор'
    )
    categories = models.ManyToManyField(
        Category,
        related_name='areas',
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
    description = models.TextField(
        max_length=2000,
        blank=True,
        verbose_name='Описание площадки'
    )
    address = models.CharField(
        max_length=255,
        verbose_name='Адрес'
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

    def __str__(self):
        return f'Площадка №{self.id}'

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
        verbose_name='автор'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='площадка'
    )
    comment = models.TextField(
        max_length=2000,
        verbose_name='комментарий'
    )
    date_added = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата добавления'
    )

    class Meta:
        ordering = ['-date_added']
        verbose_name = 'комментарий'
        verbose_name_plural = 'комментарии'


class FavoriteArea(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite'
    )
    area = models.ForeignKey(
        Area,
        on_delete=models.CASCADE,
        related_name='favorite'
    )

    class Meta:
        verbose_name = 'Избранная площадка'
        verbose_name_plural = 'Избранные площадки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'area'],
                name='unique_favorite_area'
            ),
        ]

    def __str__(self):
        return f'{self.user} {self.area}'
