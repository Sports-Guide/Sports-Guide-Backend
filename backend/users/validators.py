from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_password(value):
    if len(value) < 6:
        raise ValidationError(_(
            'Пароль должен быть больше 6ти символов'
        ))
    if len(value) > 25:
        raise ValidationError(_(
            'Пароль не должен быть больше 25 символов'
        ))
    if not any(char.islower() for char in value):
        raise ValidationError(_(
            'Пароль должен содержать одну строчную букву'
        ))
    if not any(char.isupper() for char in value):
        raise ValidationError(_(
            'Пароль должен содержать одну заглавную букву'
        ))
