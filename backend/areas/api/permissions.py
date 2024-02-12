from rest_framework import permissions


class IsAuthorOrAdminOrReadOnly(permissions.BasePermission):
    """
    Предоставляет разрешение на чтение для всех пользователей,
    но ограничивает доступ к изменению и удалению объектов только их авторам
    или администраторам.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_staff)


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Предоставляет разрешение на чтение для всех пользователей,
    но ограничивает доступ к изменению и удалению объектов
    только администраторам.
    """
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_staff)
