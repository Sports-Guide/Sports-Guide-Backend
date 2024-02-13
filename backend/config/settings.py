from datetime import timedelta
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(', ')

CSRF_TRUSTED_ORIGINS = ['https://sports-map.ru', 'http://193.107.239.81:8000']
CORS_ALLOW_ALL_ORIGINS = True
AUTH_USER_MODEL = 'users.CustomUser'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'djoser',
    'social_django',
    'users.apps.UsersConfig',
    'areas.apps.AreasConfig',
    'core.apps.CoreConfig',
    'django_filters',
    'drf_spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
if DEBUG:
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INSTALLED_APPS += ['debug_toolbar']
    INTERNAL_IPS = [
        '127.0.0.1',
    ]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'users.validators.CustomPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.'
                'NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
LANGUAGE_CODE = 'ru'
TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'areas.api.schemas.CustomSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'AUTH_HEADER_TYPES': ('Bearer',),
    "TOKEN_OBTAIN_SERIALIZER": "users.api.serializers.CustomTokenObtainPairSerializer",
}

DJOSER = {
    'SERIALIZERS': {
        'user': 'users.api.serializers.CustomUserShortSerializer',
        'current_user': 'users.api.serializers.CustomUserSerializer',
        'user_create': 'users.api.serializers.CustomUserCreateSerializer',
        'password_reset': 'users.api.serializers.CustomSendEmailResetSerializer'
    },
    'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': [os.getenv('FRONTEND_URL')],
    'PASSWORD_RESET_CONFIRM_URL': 'password/reset/confirm/{uid}/{token}',
    'ACTIVATION_URL': 'activate/{uid}/{token}',
    'SEND_ACTIVATION_EMAIL': True,
}

AUTHENTICATION_BACKENDS = (
    'social_core.backends.vk.VKOAuth2',
    'social_core.backends.yandex.YaruOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

SOCIAL_AUTH_YARU_KEY = os.getenv('YANDEX_OAUTH2_KEY')
SOCIAL_AUTH_YARU_SECRET = os.getenv('YANDEX_OAUTH2_SECRET')

SOCIAL_AUTH_VK_OAUTH2_KEY = os.getenv('VK_OAUTH2_KEY')
SOCIAL_AUTH_VK_OAUTH2_SECRET = os.getenv('VK_OAUTH2_SECRET')

SPECTACULAR_SETTINGS = {
    'TITLE': 'Sports-Map API',
    'DESCRIPTION': 'Сервис для поиска спортивных площадок',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
}

EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
