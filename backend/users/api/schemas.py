from djoser.serializers import (
    CurrentPasswordSerializer,
    SetPasswordSerializer,
    UserCreateSerializer,
)

from .serializers import CustomUserSerializer

users_data = {
    'CustomUserViewSet': {
        'tags': ['Пользователи'],
        'users_create': {
            'summary': 'Регистрация нового пользователя',
            'description': 'Создает новую учетную запись пользователя на '
                           'основе предоставленных данных, таких как имя '
                           'пользователя и пароль. После успешной регистрации '
                           'возвращает информацию о созданном пользователе.',
            'request': UserCreateSerializer,
        },
        'users_me_retrieve': {
            'summary': 'Получение данных пользователя',
            'description': 'Возвращает данные текущего пользователя. '
                           'Требуется токен аутентификации.',
        },
        'users_me_partial_update': {
            'summary': 'Обновление данных пользователя',
            'description': 'Позволяет пользователям обновлять свои данные. '
                           'Пользователь должен отправить только те поля, '
                           'которые нужно обновить. '
                           'Требуется токен аутентификации.',
            'request': CustomUserSerializer
        },
        'users_me_destroy': {
            'summary': 'Удаление учетной записи пользователя',
            'description': 'Удаляет учетную запись текущего пользователя. '
                           'Пользователь должен отправить текущий пароль. '
                           'Эта операция необратима и удаляет все данные '
                           'пользователя из системы. '
                           'Требуется токен аутентификации.',
            'request': CurrentPasswordSerializer
        },
        'users_me_upload_photo_create': {
            'summary': 'Загрузка фото пользователя',
            'description': 'Устанавливает фото для текущего пользователя. '
                           'Пользователь должен отправить фото. '
                           'Требуется токен аутентификации.',
            'request': {
                "multipart/form-data": {
                    "type": "object",
                    "properties": {
                        "photo": {"type": "string", "format": "binary"}},
                },
            },
        },
        'users_set_password_create': {
            'summary': 'Смена пароля',
            'description': 'Позволяет пользователям изменить свой текущий '
                           'пароль, предоставляя старый и новый пароль. '
                           'Требуется токен аутентификации.',
            'request': SetPasswordSerializer
        },
    }
}
