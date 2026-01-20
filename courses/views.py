from rest_framework import viewsets, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModeratorOrReadOnly, CanCreateCourse, CanDeleteObject, IsOwnerOrModeratorOrAdmin  # Импортируем созданное право

# class CourseViewSet(viewsets.ModelViewSet):
#     """
#     ViewSet для работы с курсами.
#     """
#     queryset = Course.objects.prefetch_related('lessons').all()
#     serializer_class = CourseSerializer
#     # Разрешаем чтение всем, запись - только модераторам и админам
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsModeratorOrReadOnly]
#
#     def get_permissions(self):
#         """
#         Кастомизация: создавать курсы могут только суперпользователи или админы.
#         Модераторам запрещено создавать (только редактировать существующие).
#         """
#         if self.action == 'create':
#             return [permissions.IsAuthenticated()]  # Пользователи
#         if self.action in ['update', 'partial_update']:
#             return [permissions.IsAuthenticated(), permissions.IsAdminUser()]  # Только модераторы
#         return super().get_permissions()

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с курсами с учетом ограничений для модераторов.
    """
    queryset = Course.objects.prefetch_related('lessons').all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Настраиваем permissions в зависимости от действия:
        - Создание: только не-модераторы (админы и обычные пользователи)
        - Обновление: владелец, модератор или администратор
        - Удаление: только владелец или администратор (не модератор)
        - Просмотр: все (аутентифицированные и нет)
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanCreateCourse]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrModeratorOrAdmin]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteObject]
        else:  # list, retrieve
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Оптимизируем queryset с учетом прав доступа:
        - Анонимы видят все курсы
        - Аутентифицированные видят все курсы
        """
        queryset = super().get_queryset()

        # Фильтрация по владельцу (если параметр передан)
        owner_id = self.request.query_params.get('owner_id')
        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)

        return queryset

    def perform_create(self, serializer):
        """
        Автоматически привязываем текущего пользователя как владельца курса.
        """
        # Проверяем, не является ли пользователь модератором
        is_moderator = self.request.user.groups.filter(name='moderators').exists()

        if is_moderator and not self.request.user.is_staff:
            raise PermissionError("Модераторы не могут создавать курсы")

        # Сохраняем курс с текущим пользователем в качестве владельца
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        """
        Проверяем права перед удалением курса.
        """
        # Дополнительная проверка для модераторов
        is_moderator = self.request.user.groups.filter(name='moderators').exists()

        if is_moderator and not self.request.user.is_staff:
            raise PermissionError("Модераторы не могут удалять курсы")

        # Удаляем курс
        instance.delete()


class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с уроками с учетом ограничений для модераторов.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """
        Аналогично CourseViewSet, но для уроков.
        """
        if self.action == 'create':
            permission_classes = [permissions.IsAuthenticated, CanCreateCourse]
        elif self.action in ['update', 'partial_update']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrModeratorOrAdmin]
        elif self.action == 'destroy':
            permission_classes = [permissions.IsAuthenticated, CanDeleteObject]
        else:
            permission_classes = [permissions.AllowAny]

        return [permission() for permission in permission_classes]

    def get_queryset(self):
        """
        Фильтрация уроков:
        - По курсу (course_id параметр)
        - По владельцу (owner_id параметр)
        """
        queryset = super().get_queryset()

        # Фильтрация по курсу
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)

        # Фильтрация по владельцу
        owner_id = self.request.query_params.get('owner_id')
        if owner_id:
            queryset = queryset.filter(owner_id=owner_id)

        return queryset

    def perform_create(self, serializer):
        """
        Автоматически привязываем текущего пользователя как владельца урока.
        """
        # Проверяем, не является ли пользователь модератором
        is_moderator = self.request.user.groups.filter(name='moderators').exists()

        if is_moderator and not self.request.user.is_staff:
            raise PermissionError("Модераторы не могут создавать уроки")

        # Сохраняем урок с текущим пользователем в качестве владельца
        serializer.save(owner=self.request.user)


    def perform_destroy(self, instance):
        """
        Проверяем права перед удалением урока.
        """
        # Дополнительная проверка для модераторов
        is_moderator = self.request.user.groups.filter(name='moderators').exists()

        if is_moderator and not self.request.user.is_staff:
            raise PermissionError("Модераторы не могут удалять уроки")

        # Удаляем урок
        instance.delete()