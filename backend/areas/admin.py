from django.contrib import admin

from areas.models import Area, Category, Comment


@admin.register(Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('author', 'moderation_status', 'date_added', 'description')
    list_filter = ('moderation_status', 'date_added', 'categories')
    search_fields = ('description', 'author__nickname')


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'area', 'comment', 'date_added')
    list_filter = ('date_added',)
    search_fields = ('comment', 'author__nickname', 'area__description')
    fields = ('author', 'area', 'comment', 'date_added')
