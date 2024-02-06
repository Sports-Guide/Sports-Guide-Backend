from drf_spectacular.openapi import AutoSchema
from drf_spectacular.utils import inline_serializer
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
    TokenRefreshSerializer,
    TokenVerifySerializer,
)

from areas.api.serializers import CategorySerializer, CommentSerializer
from users.api.schemas import users_data

areas_data = {
    'AreaViewSet': {
        'tags': ['Площадки'],
        'areas_list': {
            'summary': 'Получение списка площадок',
            'description': 'Возвращает список всех площадок, которые '
                           'прошли модерацию. Этот список может быть '
                           'отфильтрован по категориям.',
        },
        'areas_create': {
            'summary': 'Создание новой площадки',
            'description': 'Позволяет пользователям создавать новые площадки. '
                           'Требуется токен аутентификации.',
            'request': inline_serializer(
                name='areas_create',
                fields={
                    'latitude': serializers.DecimalField(max_digits=9,
                                                         decimal_places=6),
                    'longitude': serializers.DecimalField(max_digits=9,
                                                          decimal_places=6),
                    'categories': serializers.ListSerializer(
                        child=serializers.IntegerField()
                    )
                }
            ),
        },
        'areas_retrieve': {
            'summary': 'Получение информации о площадке',
            'description': 'Возвращает подробную информацию о конкретной '
                           'площадке.',
        },
        'areas_update': {
            'summary': 'Обновление площадки',
            'description': 'Позволяет авторам или администраторам обновлять '
                           'информацию о площадке. Требуется токен '
                           'аутентификации.',
            'request': inline_serializer(
                name='areas_update',
                fields={
                    'latitude': serializers.DecimalField(max_digits=9,
                                                         decimal_places=6),
                    'longitude': serializers.DecimalField(max_digits=9,
                                                          decimal_places=6),
                    'categories': serializers.ListSerializer(
                        child=serializers.IntegerField()
                    )
                }
            ),
        },
        'areas_partial_update': {
            'summary': 'Частичное обновление площадки',
            'description': 'Позволяет авторам или администраторам обновлять '
                           'информацию о площадке. Требуется токен '
                           'аутентификации.',
            'request': inline_serializer(
                name='areas_partial_update',
                fields={
                    'latitude': serializers.DecimalField(max_digits=9,
                                                         decimal_places=6),
                    'longitude': serializers.DecimalField(max_digits=9,
                                                          decimal_places=6),
                    'categories': serializers.ListSerializer(
                        child=serializers.IntegerField()
                    )
                }
            ),
        },
        'areas_destroy': {
            'summary': 'Удаление площадки',
            'description': 'Удаляет площадку. Эта операция доступна только '
                           'авторам области или администраторам. Требуется '
                           'токен аутентификации.',
        },
        'areas_add_images_create': {
            'summary': 'Добавление изображений к площадке',
            'description': 'Позволяет пользователям добавлять изображения '
                           'к конкретной площадке. Требуется передача файлов '
                           'изображений и доступна только для авторов '
                           'области или администраторов.',
            'request': {
                "multipart/form-data": {
                    "type": "object",
                    "properties": {
                        "image": {
                            "type": "array",
                            "items": {
                                "type": "file",
                                "format": "binary"
                            }
                        }
                    }
                }
            },
        },
        'areas_comments_retrieve': {
            'summary': 'Получение комментариев к площадке',
            'description': 'Возвращает список комментариев, оставленных '
                           'пользователями к конкретной площадке.',

        },
        'areas_my_retrieve': {
            'summary': 'Получение площадок текущего пользователя',
            'description': 'Возвращает список площадок, созданных '
                           'текущим пользователем. Требуется токен '
                           'аутентификации.',

        }
    },
    'CommentViewSet': {
        'tags': ['Комментарии'],
        'comments_list': {
            'summary': 'Получение списка комментариев',
            'description': 'Возвращает список всех комментариев.',
        },
        'comments_create': {
            'summary': 'Создание нового комментария',
            'description': 'Позволяет пользователям создавать новые '
                           'комментарии к площадкам. '
                           'Требуется токен аутентификации.',
            'request': CommentSerializer,
        },
        'comments_retrieve': {
            'summary': 'Получение информации о комментарии',
            'description': 'Возвращает подробную информацию о конкретном '
                           'комментарии.',
        },
        'comments_update': {
            'summary': 'Обновление комментария',
            'description': 'Позволяет авторам комментариев или '
                           'администраторам обновлять информацию комментария. '
                           'Требуется токен аутентификации.',
            'request': CommentSerializer,
        },
        'comments_partial_update': {
            'summary': 'Частичное обновление комментария',
            'description': 'Позволяет авторам комментариев или '
                           'администраторам частично обновлять '
                           'информацию комментария. '
                           'Требуется токен аутентификации.',
            'request': CommentSerializer,
        },
        'comments_destroy': {
            'summary': 'Удаление комментария',
            'description': 'Удаляет комментарий. Эта операция доступна только '
                           'авторам комментария или администраторам. '
                           'Требуется токен аутентификации.',
        },
    },
    'TokenObtainPairView': {
        'auth_jwt_create_create': {
            'summary': 'Создание токена JWT',
            'description': 'Позволяет пользователю получить токен JWT, '
                           'предоставив учетные данные. Этот токен '
                           'используется для аутентификации запросов.',
            'request': TokenObtainPairSerializer
        }
    },
    'TokenRefreshView': {
        'auth_jwt_refresh_create': {
            'summary': 'Обновление токена JWT',
            'description': 'Позволяет обновить существующий токен JWT. '
                           'Для этого необходимо предоставить действующий '
                           'refresh токен.',
            'request': TokenRefreshSerializer
        }
    },
    'TokenVerifyView': {
        'auth_jwt_verify_create': {
            'summary': 'Проверка токена JWT',
            'description': 'Позволяет проверить действительность токена JWT. '
                           'Для этого необходимо предоставить токен, '
                           'который нужно проверить.',
            'request': TokenVerifySerializer
        }
    },
    'CategoryViewSet': {
        'tags': ['Категории'],
        'categories_list': {
            'summary': 'Получение списка категорий',
            'description': 'Возвращает список всех категорий.',
        },
        'categories_create': {
            'summary': 'Создание новой категории',
            'description': 'Позволяет администраторам создавать новые '
                           'категории. Требуется токен аутентификации.',
            'request': CategorySerializer,
        },
        'categories_retrieve': {
            'summary': 'Получение информации о категории',
            'description': 'Возвращает информацию о конкретной категории.',
        },
        'categories_update': {
            'summary': 'Обновление категории',
            'description': 'Позволяет администраторам обновлять информацию о '
                           'категории. Требуется токен аутентификации.',
            'request': CategorySerializer,
        },
        'categories_partial_update': {
            'summary': 'Частичное обновление категории',
            'description': 'Позволяет администраторам обновлять информацию о '
                           'категории. Требуется токен аутентификации.',
            'request': CategorySerializer,
        },
        'categories_destroy': {
            'summary': 'Удаление категории',
            'description': 'Удаляет категорию. Эта операция доступна только '
                           'администраторам. Требуется токен аутентификации.',
        },
    }
}

data = {'default': {'tags': ['Аутентификация']}} | areas_data | users_data


class CustomSchema(AutoSchema):
    def get_tags(self):
        try:
            return data[self.view.__class__.__name__]['tags']
        except KeyError:
            return data['default']['tags']

    def get_description(self):
        try:
            return data[self.view.__class__.__name__][
                self.get_operation_id().lower()]['description']
        except KeyError:
            return None

    def get_summary(self):
        try:
            return data[self.view.__class__.__name__][
                self.get_operation_id().lower()]['summary']
        except KeyError:
            return None

    def get_request_serializer(self):
        try:
            return data[self.view.__class__.__name__][
                self.get_operation_id().lower()]['request']
        except KeyError:
            return None
