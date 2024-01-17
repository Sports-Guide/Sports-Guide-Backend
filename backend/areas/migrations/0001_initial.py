# Generated by Django 4.2.8 on 2024-01-16 18:58

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


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
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Широта')),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9, verbose_name='Долгота')),
                ('moderation_status', models.CharField(choices=[('rejected', 'Отклонено'), ('pending', 'На рассмотрении'), ('approved', 'Одобрено')], default='pending', max_length=10, verbose_name='статус модерации')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
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
                ('name', models.CharField(max_length=255, verbose_name='название')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(verbose_name='комментарий')),
                ('date_added', models.DateTimeField(auto_now_add=True, verbose_name='дата добавления')),
                ('area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='areas.area', verbose_name='площадка')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='автор')),
            ],
            options={
                'verbose_name': 'комментарий',
                'verbose_name_plural': 'комментарии',
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
            field=models.ManyToManyField(to='areas.category', verbose_name='категории'),
        ),
    ]
