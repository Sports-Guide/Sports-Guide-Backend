from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet

app_name = 'users'

router = DefaultRouter()

router.register(r'users', CustomUserViewSet, basename='customuser')

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
