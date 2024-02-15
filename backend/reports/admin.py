from django.contrib import admin

from .models import Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'report_type',
        'wrong_info',
        'other_info',
        'latitude',
        'longitude',
        'user'
    ]
