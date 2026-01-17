from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonCreateView, LessonListView, LessonRetrieveView, LessonUpdateView, LessonDestroyView
)

app_name = 'courses'

router = DefaultRouter()
router.register(r'courses', CourseViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('lessons/create', LessonCreateView.as_view(), name='lesson-create'),
    path('lessons/', LessonListView.as_view(), name='lesson-list'),
    path('lessons/<int:pk>/detail', LessonRetrieveView.as_view(), name='lesson-detail'),
    path('lessons/<int:pk>/update', LessonUpdateView.as_view(), name='lesson-update'),
    path('lessons/<int:pk>/delete', LessonDestroyView.as_view(), name='lesson-delete'),
] + router.urls