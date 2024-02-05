from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.api.views import CustomUserViewSet

app_name = 'users'

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='customuser')

urlpatterns = [
    path('users/',
         CustomUserViewSet.as_view({'post': 'create'}),
         name='register'),
    path('users/set_password/',
         CustomUserViewSet.as_view({'post': 'set_password'}),
         name='set_password'),
    path('users/me/',
         CustomUserViewSet.as_view({
             'get': 'me',
             'patch': 'me',
             'delete': 'me'}),
         name='me'),
    path('users/me/upload_photo/',
         CustomUserViewSet.as_view({'post': 'upload_photo'}),
         name='upload_photo'),
    path('users/reset_password/',
         CustomUserViewSet.as_view({'post': 'reset_password'}),
         name='reset_password'),
    path('users/reset_password_confirm/',
         CustomUserViewSet.as_view({'post': 'reset_password_confirm'}),
         name='reset_password_confirm'),
    path('users/activation/',
         CustomUserViewSet.as_view({'post': 'activation'}),
         name='activation'),
    path('users/resend_activation/',
         CustomUserViewSet.as_view({'post': 'resend_activation'}),
         name='resend_activation'),
    # path('auth/', include('djoser.urls')),
    # path('auth/', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
