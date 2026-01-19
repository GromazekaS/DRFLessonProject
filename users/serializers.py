from rest_framework import serializers
from .models import Payment, User
from courses.serializers import LessonSerializer, CourseSerializer
from courses.models import Course, Lesson


class PaymentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(
        source='paid_course.title',
        read_only=True,
        allow_null=True
    )

    lesson_title = serializers.CharField(
        source='paid_lesson.title',
        read_only=True,
        allow_null=True
    )

    user_email = serializers.CharField(
        source='user.email',
        read_only=True
    )

    class Meta:
        model = Payment
        fields = '__all__'
        #     [
        #     'id',
        #     'user',
        #     'user_email',
        #     'payment_date',
        #     'paid_course',
        #     'course_title',
        #     'paid_lesson',
        #     'lesson_title',
        #     'amount',
        #     'payment_method',
        # ]
        read_only_fields = ['user', 'payment_date']


class UserSerializer(serializers.ModelSerializer):
    enrolled_courses = serializers.SerializerMethodField()
    enrolled_lessons = serializers.SerializerMethodField()
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'phone', 'city', 'avatar',
            'enrolled_courses', 'enrolled_lessons', 'payments'
        ]

    def get_enrolled_courses(self, obj):
        """Получаем курсы из платежей пользователя"""
        # Получаем ID оплаченных курсов
        paid_course_ids = obj.payments.filter(
            paid_course__isnull=False
        ).values_list('paid_course_id', flat=True).distinct()

        # Получаем объекты курсов
        courses = Course.objects.filter(id__in=paid_course_ids)

        return CourseSerializer(courses, many=True, context=self.context).data

    def get_enrolled_lessons(self, obj):
        """Получаем уроки из платежей пользователя"""
        # Получаем ID оплаченных уроков
        paid_lesson_ids = obj.payments.filter(
            paid_lesson__isnull=False
        ).values_list('paid_lesson_id', flat=True).distinct()

        # Получаем объекты уроков
        lessons = Lesson.objects.filter(id__in=paid_lesson_ids)

        return LessonSerializer(lessons, many=True, context=self.context).data

