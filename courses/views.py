from rest_framework import viewsets, generics
from .models import Course, Lesson
from .serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer


class LessonCreateView(generics.CreateAPIView):
    serializer_class = LessonSerializer

class LessonListView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonRetrieveView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonUpdateView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

class LessonDestroyView(generics.DestroyAPIView):
    serializer_class = LessonSerializer
