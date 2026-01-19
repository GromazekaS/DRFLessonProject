from rest_framework import viewsets, permissions
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer
from users.permissions import IsModeratorOrReadOnly  # Импортируем созданное право

class CourseViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с курсами.
    """
    queryset = Course.objects.prefetch_related('lessons').all()
    serializer_class = CourseSerializer
    # Разрешаем чтение всем, запись - только модераторам и админам
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsModeratorOrReadOnly]

    def get_permissions(self):
        """
        Кастомизация: создавать курсы могут только суперпользователи или админы.
        Модераторам запрещено создавать (только редактировать существующие).
        """
        if self.action == 'create':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]  # Только админы
        return super().get_permissions()

class LessonViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с уроками.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsModeratorOrReadOnly]

    def get_permissions(self):
        """
        Аналогично курсам: создавать уроки могут только админы.
        """
        if self.action == 'create':
            return [permissions.IsAuthenticated(), permissions.IsAdminUser()]
        return super().get_permissions()