from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'email',
        'nickname',
        'get_photo',
        'is_staff',
        'is_active',
        'date_joined',
    )
    search_fields = (
        'email',
        'nickname',
    )
    empty_value_display = '-пусто-'
    readonly_fields = ("get_photo",)

    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f'<img src={obj.photo.url} width="50"')
        return "Без фото"

    get_photo.short_description = "Изображение"
