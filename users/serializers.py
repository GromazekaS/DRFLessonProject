from rest_framework import serializers
from .models import Payment, User
from courses.serializers import LessonSerializer, CourseSerializer
from courses.models import Course, Lesson


class PaymentSerializer(serializers.ModelSerializer):
    course_title = serializers.CharField(source='paid_course.title', read_only=True)

    class Meta:
        model = Payment
        fields = [
            'id',
            'payment_date',
            'amount',
            'payment_method',
            'course_title',
            'payment_link',
            'status'
        ]
        read_only_fields = fields


class UserPublicSerializer(serializers.ModelSerializer):
    """
    Упрощенный сериализатор для отображения в списке пользователей (для модераторов).
    Не включает чувствительные данные.
    """
    class Meta:
        model = User
        fields = ['id', 'email', 'phone', 'city', 'avatar']

class UserSerializer(serializers.ModelSerializer):
    """
    Полный сериализатор для владельца и модераторов.
    """
    enrolled_courses = CourseSerializer(many=True, read_only=True)
    enrolled_lessons = LessonSerializer(many=True, read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'id', 'email', 'password', 'phone', 'city', 'avatar',
            'enrolled_courses', 'enrolled_lessons', 'payments'
        ]
        extra_kwargs = {
            'password': {'write_only': True}  # Пароль не отображается при чтении
        }

    def create(self, validated_data):
        """ Создание пользователя с хешированием пароля. """
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        """ Обновление пользователя с хешированием пароля при изменении. """
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance