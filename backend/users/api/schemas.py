from djoser.serializers import (
    ActivationSerializer,
    CurrentPasswordSerializer,
    PasswordResetConfirmSerializer,
    UserCreateSerializer,
)

from .serializers import CustomSendEmailResetSerializer, CustomUserSerializer

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
        'users_activation_create': {
            'summary': 'Активация учетной записи пользователя',
            'description': 'Активирует учетную запись пользователя через '
                           'токен активации, отправленный на электронный '
                           'адрес после регистрации. Требуется токен '
                           'активации, отправленный по электронной почте.',
            'request': ActivationSerializer
        },
        'users_resend_activation_create': {
            'summary': 'Повторная отправка письма активации',
            'description': 'В случае, если письмо активации не было получено '
                           'или потеряно, пользователь может запросить его '
                           'повторную отправку. Необходимо указать '
                           'электронный адрес, связанный с учетной записью.',
            'request': CustomSendEmailResetSerializer
        },
        'users_reset_password_create': {
            'summary': 'Инициация сброса пароля',
            'description': 'Позволяет пользователю запросить сброс пароля, '
                           'отправив электронный адрес, связанный с учетной '
                           'записью. На указанный адрес будет отправлено '
                           'письмо со ссылкой для создания нового пароля. '
                           'Требуется ввод электронного адреса, '
                           'связанного с учетной записью.',
            'request': CustomSendEmailResetSerializer
        },
        'users_reset_password_confirm_create': {
            'summary': 'Подтверждение сброса пароля',
            'description': 'Завершает процесс сброса пароля. Пользователь '
                           'должен предоставить токен сброса пароля, '
                           'полученный в письме, и новый пароль. '
                           'Требуется токен сброса и новый пароль.',
            'request': PasswordResetConfirmSerializer
        },

    }
}
