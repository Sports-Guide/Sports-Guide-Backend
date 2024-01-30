import random

from django.contrib.auth import get_user_model
import factory
from faker import Faker

from .constants import ModerationStatus
from .models import Area, Category, Comment

fake = Faker("ru_RU")
User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    email = factory.Sequence(lambda n: f'user{n}@sports-map.ru')
    nickname = factory.Sequence(lambda n: f'sport-user{n}')
    password = factory.PostGenerationMethodCall('set_password', 'password')


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: f'category{n}')
    slug = factory.LazyAttribute(lambda obj: f'slug-{obj.name}')


class AreaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Area

    author = factory.SubFactory(UserFactory)
    latitude = factory.LazyFunction(lambda: random.uniform(55.70, 55.80))
    longitude = factory.LazyFunction(lambda: random.uniform(37.55, 37.70))
    moderation_status = ModerationStatus.APPROVED.value

    @factory.post_generation
    def categories(self, create, extracted, **kwargs):
        if not create:
            # Если мы используем 'build' вместо 'create'
            return

        if extracted:
            # Если переданы конкретные категории при создании объекта
            for category in extracted:
                self.categories.add(category)
        else:
            # Добавляем случайное количество категорий
            num_categories = random.randint(1,
                                            5)  # Например, от 1 до 5 категорий
            categories = CategoryFactory.create_batch(num_categories)
            for category in categories:
                self.categories.add(category)


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.SubFactory(UserFactory)
    area = factory.SubFactory(AreaFactory)
    comment = factory.LazyFunction(lambda: fake.sentence())
