from rest_framework import viewsets, permissions, status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Lesson, Subscription
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
    # permission_classes = [permissions.IsAuthenticated] #permissions.IsAuthenticatedOrReadOnly, IsModeratorOrReadOnly]

    def get_permissions(self):
        """
        Аналогично курсам: создавать уроки могут только админы.
        """
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return [] # [permissions.IsAuthenticated()] #, permissions.IsAdminUser()]
        return [permissions.IsAuthenticated()]


class SubscriptionAPIView(APIView):
    """
    Простой APIView для управления подпиской на курс.
    POST запрос переключает состояние подписки:
    - Если подписки нет → создает
    - Если подписка есть → удаляет
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        """
        Переключает состояние подписки пользователя на курс.
        Возвращает текущий статус подписки после выполнения.
        """
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        # Проверяем существующую подписку
        subscription = Subscription.objects.filter(
            user=user,
            course=course
        ).first()

        if subscription:
            # Если подписка есть - удаляем (отписываемся)
            subscription.delete()
            is_subscribed = False
            message = "Подписка удалена"
        else:
            # Если подписки нет - создаем (подписываемся)
            Subscription.objects.create(user=user, course=course)
            is_subscribed = True
            message = "Подписка добавлена"

        return Response({
            "course_id": course.id,
            "course_title": course.title,
            "is_subscribed": is_subscribed,
            "message": message
        }, status=status.HTTP_200_OK)

    def get(self, request, course_id=None):
        """
        Проверяет статус подписки пользователя на курс.
        Если course_id не указан - возвращает все подписки пользователя.
        """
        user = request.user

        if course_id:
            # Проверяем подписку на конкретный курс
            course = get_object_or_404(Course, id=course_id)
            is_subscribed = Subscription.objects.filter(
                user=user,
                course=course
            ).exists()

            return Response({
                "course_id": course.id,
                "course_title": course.title,
                "is_subscribed": is_subscribed
            })
        else:
            # Возвращаем все курсы, на которые подписан пользователь
            subscriptions = Subscription.objects.filter(user=user)
            subscribed_courses = [sub.course for sub in subscriptions]

            # Используем CourseSerializer для сериализации
            from .serializers import CourseSerializer
            serializer = CourseSerializer(
                subscribed_courses,
                many=True,
                context={'request': request}
            )

            return Response({
                "count": subscriptions.count(),
                "results": serializer.data
            })