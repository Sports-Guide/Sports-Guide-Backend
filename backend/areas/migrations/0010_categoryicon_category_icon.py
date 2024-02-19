# Generated by Django 4.2.8 on 2024-02-19 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('areas', '0009_alter_area_latitude_alter_area_longitude'),
    ]

    operations = [
        migrations.CreateModel(
            name='CategoryIcon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='название')),
                ('image', models.ImageField(upload_to='category_icons/', verbose_name='изображение')),
            ],
            options={
                'verbose_name': 'иконка',
                'verbose_name_plural': 'иконки',
            },
        ),
        migrations.AddField(
            model_name='category',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='areas.categoryicon', verbose_name='иконка'),
        ),
    ]
