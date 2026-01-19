# permissions.py (например, в папке приложения users)
from rest_framework import permissions
from django.contrib.auth.models import Group

class IsModerator(permissions.BasePermission):
    """
    Проверяет, является ли пользователь модератором или администратором.
    """
    def has_permission(self, request, view):
        # Проверяем, аутентифицирован ли пользователь
        if not request.user or not request.user.is_authenticated:
            return False
        # Проверяем, состоит ли пользователь в группе "moderators" или является суперпользователем
        return (request.user.groups.filter(name='moderators').exists() or
                request.user.is_staff or
                request.user.is_superuser)

class IsOwner(permissions.BasePermission):
    """
    Разрешает доступ только владельцу объекта.
    Предполагается, что у модели есть атрибут 'owner' (ForeignKey на User).
    Если атрибут называется иначе (например, 'user', 'author'), измените getattr.
    """
    def has_object_permission(self, request, view, obj):
        # Разрешаем GET, HEAD, OPTIONS запросы от владельца
        if request.method in permissions.SAFE_METHODS:
            return True
        # Сравниваем владельца объекта с текущим пользователем
        return getattr(obj, 'user', None) == request.user

class IsModeratorOrReadOnly(permissions.BasePermission):
    """
    Разрешает полный доступ модераторам и админам.
    Остальным пользователям разрешены только безопасные методы (GET, HEAD, OPTIONS).
    """
    def has_permission(self, request, view):
        # Всегда разрешаем безопасные запросы
        if request.method in permissions.SAFE_METHODS:
            return True
        # Для изменяющих запросов проверяем права модератора
        return (request.user.is_authenticated and
                (request.user.groups.filter(name='moderators').exists() or
                 request.user.is_staff or
                 request.user.is_superuser))