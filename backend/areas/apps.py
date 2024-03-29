from django.apps import AppConfig


class AreasConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'areas'
    verbose_name = 'Управление площадками'

    def ready(self):
        import areas.signals  # noqa
