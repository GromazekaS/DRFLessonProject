from rest_framework import serializers
from .models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    course_title = serializers.CharField(source='course.title', read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'preview', 'video_url',
            'course', 'course_title', 'owner', 'owner_email',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'owner_email', 'created_at', 'updated_at']


class CourseSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    owner_email = serializers.EmailField(source='owner.email', read_only=True)
    lesson_count = serializers.IntegerField(source='lessons.count', read_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id', 'title', 'preview', 'description', 'price',
            'owner', 'owner_email', 'lessons', 'lesson_count',
            'is_subscribed', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'owner_email', 'created_at', 'updated_at']

    def get_lesson_count(self, obj):
        return obj.lessons.count()