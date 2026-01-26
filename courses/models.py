from django.db import models
from django.utils import timezone
from rest_framework import serializers
from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    preview = models.ImageField(upload_to='courses/previews/', blank=True, null=True, verbose_name='Превью')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=10000.00,
        verbose_name='Стоимость курса'
    )
    created_at = models.DateTimeField(
        default=timezone.now,  # Без скобок!
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        default=timezone.now,  # Без скобок!
        verbose_name='Дата создания'
    )
    # ПОЛЯ ДЛЯ РАССЫЛКИ:
    last_updated = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Время последнего обновления (для подписчиков)'
    )
    owner = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='owned_courses',
                             verbose_name='Владелец')
    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    preview = models.ImageField(upload_to='lessons/previews/', blank=True, null=True, verbose_name='Превью')
    video_link = models.URLField(verbose_name='Ссылка на видео', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name='Курс')
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=10000.00,
        verbose_name='Стоимость курса'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    course = models.ForeignKey('courses.Course', on_delete=models.CASCADE, verbose_name='Курс')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата подписки')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        unique_together = ['user', 'course']  # Один пользователь - одна подписка на курс

    def __str__(self):
        return f'{self.user.email} → {self.course.title}'