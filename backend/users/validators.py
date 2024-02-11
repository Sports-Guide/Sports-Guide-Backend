from django.core.exceptions import ValidationError


class CustomPasswordValidator:
    """
    Валидатор пароля пользователя.
    """
    def validate(self, password, user=None):
        if not any(char.islower() for char in password):
            raise ValidationError('Пароль должен содержать хотя бы '
                                  'один символ в нижнем регистре.')

        if not any(char.isupper() for char in password):
            raise ValidationError('Пароль должен содержать хотя бы '
                                  'один символ в верхнем регистре.')

        if not all(ord(char) < 128 for char in password):
            raise ValidationError(
                'Пароль может содержать только латинские символы.',
                code='password_no_latin'
            )

        if len(password) > 25:
            raise ValidationError(
                'Введённый пароль слишком длинный. '
                'Он не должен содержать больше 25 символов.'
            )
