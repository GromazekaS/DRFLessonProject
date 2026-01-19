from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonViewSet,
)

app_name = 'courses'

router = DefaultRouter()
router.register(r'courses', CourseViewSet)
router.register(r'lessons', LessonViewSet)

urlpatterns = [
#    path('', include(router.urls)),
] + router.urls