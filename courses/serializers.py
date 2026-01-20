from rest_framework import serializers
from .models import Course, Lesson
from .validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link', 'course']
        validators = [LinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    lesson_count = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'preview', 'description', 'lesson_count', 'lessons']

    def get_lesson_count(self, obj):
        return obj.lessons.count()