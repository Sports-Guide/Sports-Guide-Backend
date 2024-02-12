from django.contrib import admin

from areas.models import Area, AreaImage, Category, Comment


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
