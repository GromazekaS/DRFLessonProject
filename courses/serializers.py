from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'preview', 'video_link', 'course']
        validators = [LinkValidator(field='video_link')]


class CourseSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ['id', 'title', 'description', 'preview', 'is_subscribed']

    def get_is_subscribed(self, obj):
        """Проверяем, подписан ли текущий пользователь на этот курс"""
        request = self.context.get('request')

        if request and request.user.is_authenticated:
            return Subscription.objects.filter(
                user=request.user,
                course=obj
            ).exists()
        return False