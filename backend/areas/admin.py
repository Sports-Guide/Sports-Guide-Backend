from django.contrib import admin

from areas.models import Area, AreaImage, Category, Comment


class AreaImageInline(admin.TabularInline):
    model = AreaImage
    extra = 1


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('author', 'moderation_status', 'date_added',)
    list_filter = ('moderation_status', 'date_added', 'categories',)
    search_fields = ('author__nickname',)
    inlines = (AreaImageInline,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'area', 'comment', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('comment', 'author__nickname',)
