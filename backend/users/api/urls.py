from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.api.views import CustomUserViewSet

app_name = 'users'

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='customuser')

urlpatterns = [
    path(
        'users/register/',
        CustomUserViewSet.as_view({'post': 'create'}),
        name='register'
    ),
    path(
        'users/set_password/',
        CustomUserViewSet.as_view({'post': 'set_password'}),
        name='set_password'
    ),
    path(
        'users/me/',
        CustomUserViewSet.as_view({
            'get': 'me',
            'patch': 'me',
            'delete': 'me'
        }),
        name='me'
    ),
    path(
        'users/me/upload_photo/',
        CustomUserViewSet.as_view({'post': 'upload_photo'}),
        name='upload_photo'
    ),
    path('auth/', include('djoser.urls')),
    path('auth/', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
