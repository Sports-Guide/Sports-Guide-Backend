from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserCreateViewSet

router = DefaultRouter()
router.register(r"users", CustomUserCreateViewSet, basename="user")

urlpatterns = [
    path("auth/", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
