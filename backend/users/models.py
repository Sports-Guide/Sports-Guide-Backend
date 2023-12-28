from django.db import models

from django.core.validators import MinLengthValidator
from .validators import validate_password

from django.contrib.auth.models import AbstractBaseUser
from .manager import CustomUserManager
from django.contrib.auth.models import PermissionsMixin


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        'Электронная почта',
        max_length=50,
        unique=True
        )
    nickname = models.SlugField(
        'Ник',
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(6)]
    )
    photo = models.ImageField(
        'Аватар',
        upload_to='users_photo/',
        blank=True,
        null=True
    )
    password = models.CharField(
        'Пароль',
        validators=[validate_password],
        max_length=25
    )
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'nickname'

    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    def __str__(self):
        return f'{self.nickname}'
