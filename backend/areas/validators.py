import re

from django.core.exceptions import ValidationError


def validate_category_name(value):
    """
    Валидатор названия категории.
    """
    if not re.match(r'^[А-Яа-яA-Za-z\-\s\(\)]+$', value):
        raise ValidationError(
            'Название может содержать только символы кириллицы, латиницы, '
            'дефис, пробел и круглые скобки.')
