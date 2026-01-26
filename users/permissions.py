from rest_framework import permissions
from django.contrib.auth.models import Group

# class IsModerator(permissions.BasePermission):
#     """
#     Проверяет, является ли пользователь модератором или администратором.
#     """
#     def has_permission(self, request, view):
#         # Проверяем, аутентифицирован ли пользователь
#         if not request.user or not request.user.is_authenticated:
#             return False
#         # Проверяем, состоит ли пользователь в группе "moderators" или является суперпользователем
#         return (request.user.groups.filter(name='moderators').exists() or
#                 request.user.is_staff or
#                 request.user.is_superuser)

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

class IsModerator(permissions.BasePermission):
    """Проверка, является ли пользователь модератором"""

    def has_permission(self, request, view):
        return request.user.is_authenticated and self._is_moderator(request.user)

    def _is_moderator(self, user):
        """Проверка через метод exists для получения булева значения"""
        return user.groups.filter(name='moderators').exists()

class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):
    """
    Разрешает доступ владельцу, модератору или администратору.
    Модератору разрешено только чтение и обновление, но не создание/удаление.
    """

    def has_object_permission(self, request, view):
        # Разрешаем безопасные методы (GET, HEAD, OPTIONS) всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Проверяем, является ли пользователь владельцем
        obj = view.get_object()
        is_owner = obj.owner == request.user if hasattr(obj, 'owner') else False

        # Проверяем, является ли пользователь модератором
        is_moderator = request.user.is_authenticated and request.user.groups.filter(name='moderators').exists()

        # Проверяем, является ли пользователь администратором
        is_admin = request.user.is_staff

        # Для методов обновления разрешаем владельцу, модератору и администратору
        if request.method in ['PUT', 'PATCH']:
            return is_owner or is_moderator or is_admin

        # Для метода DELETE разрешаем только владельцу и администратору
        elif request.method == 'DELETE':
            return is_owner or is_admin

        return False

class CanCreateCourse(permissions.BasePermission):
    """Разрешает создание курсов только не-модераторам и администраторам"""

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Проверяем, является ли пользователь модератором
        is_moderator = request.user.groups.filter(name='moderators').exists()

        # Модераторы не могут создавать курсы
        if is_moderator and not request.user.is_staff:
            return False

        return True

class CanDeleteObject(permissions.BasePermission):
    """Разрешает удаление только владельцам и администраторам"""

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False

        # Проверяем владельца
        is_owner = obj.owner == request.user if hasattr(obj, 'owner') else False

        # Администраторы могут удалять
        if request.user.is_staff:
            return True

        # Владельцы могут удалять свои объекты
        return is_owner