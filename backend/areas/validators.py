import re

from django.core.exceptions import ValidationError


def validate_category_name(value):
    if not re.match(r'^[А-Яа-яA-Za-z\- ]+$', value):
        raise ValidationError(
            'Название может содержать только символы кириллицы, латиницы, '
            'дефис и пробел.')
