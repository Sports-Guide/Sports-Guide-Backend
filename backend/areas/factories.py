import factory
from django.contrib.auth import get_user_model

from .constants import ModerationStatus
from .models import Area, Category, Comment

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


class AreaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Area

    author = factory.SubFactory(UserFactory)
    latitude = 55.7558
    longitude = 37.6173
    moderation_status = ModerationStatus.PENDING.value


class CommentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Comment

    author = factory.SubFactory(UserFactory)
    area = factory.SubFactory(AreaFactory)
    comment = "Sample comment"
