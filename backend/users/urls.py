from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

router = DefaultRouter()
router.register(r"users", CustomUserViewSet, basename="user")

urlpatterns = [
    path("auth/", include(router.urls)),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
]
