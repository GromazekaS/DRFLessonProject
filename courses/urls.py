from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonViewSet,
    SubscriptionAPIView,
)

app_name = 'courses'

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
    # Эндпоинт для управления подпиской на конкретный курс
    path('courses/<int:course_id>/subscription/', SubscriptionAPIView.as_view(), name='course-subscription'),

    # Эндпоинт для получения всех подписок пользователя
    path('my-subscriptions/', SubscriptionAPIView.as_view(), name='my-subscriptions'),
] + router.urls