from django.contrib import admin

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "nickname",
        "photo",
        "is_staff",
        "is_active",
        "date_joined",
        "password",
    )
    search_fields = (
        "email",
        "nickname",
    )
    empty_value_display = "-пусто-"
