# Generated by Django 4.2.8 on 2024-02-06 18:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('areas', '0005_alter_area_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='area_name',
            field=models.CharField(default=1, max_length=50, verbose_name='название площадки'),
            preserve_default=False,
        ),
    ]