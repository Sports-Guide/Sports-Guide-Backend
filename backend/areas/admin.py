from django.contrib import admin
from django.utils.html import format_html_join, mark_safe

from areas.models import Area, AreaImage, Category, Comment, Report


class AreaImageInline(admin.TabularInline):
    model = AreaImage
    extra = 1


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    """
    Конфигурация панели администратора для площадок.
    """
    list_display = (
        'author',
        'moderation_status',
        'date_added',
        'added_to_favorites'
    )
    list_filter = ('moderation_status', 'date_added', 'categories',)
    search_fields = ('author__nickname',)
    inlines = (AreaImageInline,)

    def added_to_favorites(self, obj: Area):
        """
        Метод для отображения количества добавлений площадки в избранное.
        """
        return obj.favorite.count()


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Конфигурация панели администратора для категорий.
    """
    list_display = ('name',)
    search_fields = ('name',)
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Конфигурация панели администратора для комментариев.
    """
    list_display = ('author', 'area', 'comment', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('comment', 'author__nickname',)


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'area',
        'report_type',
        'description',
        'latitude',
        'longitude',
        'user',
        'display_images'
    ]

    def display_images(self, obj):
        images = obj.images.all()
        if not images:
            return 'Нет фото'
        return mark_safe(format_html_join(
            '\n', "<img src='{}' width='50'>",
            ((image.image.url,) for image in images)
        ))
    display_images.short_description = 'Images'
