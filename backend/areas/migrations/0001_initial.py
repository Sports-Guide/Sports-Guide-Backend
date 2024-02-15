# Generated by Django 4.2.8 on 2024-02-15 06:22

import areas.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=15, max_digits=18, verbose_name='Широта')),
                ('longitude', models.DecimalField(decimal_places=15, max_digits=18, verbose_name='Долгота')),
                ('description', models.TextField(blank=True, max_length=2000, verbose_name='Описание площадки')),
                ('address', models.CharField(max_length=255, verbose_name='Адрес')),
                ('moderation_status', models.CharField(choices=[('rejected', 'Отклонено'), ('pending', 'На рассмотрении'), ('approved', 'Одобрено')], default='pending', max_length=10, verbose_name='статус модерации')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='areas', to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'площадка',
                'verbose_name_plural': 'площадки',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, validators=[django.core.validators.MinLengthValidator(3), areas.validators.validate_category_name], verbose_name='название')),
                ('area_name', models.CharField(max_length=50, verbose_name='название площадки')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='уникальный тег')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_type', models.CharField(choices=[('WRONG_INFO', 'Неправильная информация'), ('CLOSED', 'Площадка закрылась'), ('CHANGE_COORDS', 'Уточнить местоположение'), ('OTHER', 'Другое')], max_length=20)),
                ('description', models.TextField(blank=True, max_length=256, null=True, verbose_name='неправильная информация')),
                ('images', models.ImageField(upload_to='area_images/', verbose_name='изображение')),
                ('latitude', models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True, verbose_name='Широта')),
                ('longitude', models.DecimalField(blank=True, decimal_places=15, max_digits=18, null=True, verbose_name='Долгота')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='areas.area', verbose_name='площадка')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'уточнение информации',
                'verbose_name_plural': 'уточнение информации',
            },
        ),
        migrations.CreateModel(
            name='FavoriteArea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to='areas.area')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorite', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Избранная площадка',
                'verbose_name_plural': 'Избранные площадки',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(max_length=2000, verbose_name='комментарий')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='areas.area', verbose_name='площадка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии',
                'ordering': ['-date_added'],
            },
        ),
        migrations.CreateModel(
            name='AreaImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='area_images/', verbose_name='изображение')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='areas.area', verbose_name='площадка')),
            ],
            options={
                'verbose_name': 'фото площадки',
                'verbose_name_plural': 'фото площадок',
            },
        ),
        migrations.AddField(
            model_name='area',
            name='categories',
            field=models.ManyToManyField(related_name='areas', to='areas.category', verbose_name='категории'),
        ),
        migrations.AddConstraint(
            model_name='favoritearea',
            constraint=models.UniqueConstraint(fields=('user', 'area'), name='unique_favorite_area'),
        ),
    ]
