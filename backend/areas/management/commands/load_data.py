from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from areas.factories import CommentFactory

User = get_user_model()


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            email = 'admin@sports-map.ru'
            nickname = 'admin'
            password = 'admin'
            if not User.objects.filter(email=email).exists():
                User.objects.create_superuser(
                    email=email,
                    nickname=nickname,
                    password=password
                )

            for _ in range(20):
                CommentFactory.create()

            self.stdout.write(
                self.style.SUCCESS('Тестовые данные успешно загружены.'))
        except IntegrityError:
            self.stdout.write('Ошибка. Тестовые данные уже загружены.')
