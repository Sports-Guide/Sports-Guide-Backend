from django.urls import include, path
from djoser.serializers import UserSerializer
urlpatterns = [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
