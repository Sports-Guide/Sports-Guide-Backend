from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import CustomUserViewSet

app_name = 'users'

router = DefaultRouter()

router.register('users', CustomUserViewSet)

urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('', include(router.urls)),
    path('auth/', include('djoser.urls.jwt')),
]
