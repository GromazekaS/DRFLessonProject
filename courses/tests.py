from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from courses.models import Course, Lesson, Subscription

User = get_user_model()


class SimpleTestCase(APITestCase):
    """
    Простые тесты для проверки работы системы.
    """

    def setUp(self):
        self.client = APIClient()

        # СПОСОБ 1: Создаем через User() и save()
        self.user = User(
            email='user@test.com',
            first_name='Иван',
            last_name='Иванов'
        )
        self.user.set_password('testpass123')  # Важно: set_password
        self.user.save()

        # СПОСОБ 2: Суперпользователя тоже создаем напрямую
        self.admin = User(
            email='admin@test.com',
            is_staff=True,
            is_superuser=True
        )
        self.admin.set_password('adminpass123')
        self.admin.save()

        # Создаем курс
        self.course = Course.objects.create(
            title='Тестовый курс',
            description='Описание тестового курса',
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            title='Тестовый урок',
            description='Описание тестового урока',
            course=self.course,
            video_link='https://www.youtube.com/watch?v=test123'
        )

        # URL для тестирования
        self.lessons_url = reverse('courses:lesson-list')
        self.lesson_detail_url = reverse('courses:lesson-list', args=[self.lesson.id])

    def test_user_creation(self):
        """Тест создания пользователя."""
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(self.user.email, 'user@test.com')
        self.assertTrue(self.user.check_password('testpass123'))
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_user_can_view_lessons(self):
        """Аутентифицированный пользователь может просматривать уроки."""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lessons_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_admin_can_create_lesson(self):
        """Администратор может создать урок."""
        self.client.force_authenticate(user=self.admin)
        data = {
            'title': 'Новый урок',
            'description': 'Описание нового урока',
            'course': self.course.id,
            'video_link': 'https://www.youtube.com/watch?v=new'
        }
        response = self.client.post(self.lessons_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class SubscriptionTests(APITestCase):
    """Тесты для подписок."""

    def setUp(self):
        self.client = APIClient()

        # Просто создаем пользователей через конструктор
        self.user = User(email='user@test.com')
        self.user.set_password('testpass123')
        self.user.save()

        self.course = Course.objects.create(
            title='Курс для подписок',
            description='Описание',
        )

        # URL
        self.subscribe_url = reverse('courses:course-subscription', args=[self.course.id])

    def test_subscribe_and_unsubscribe(self):
        """Тест подписки и отписки."""
        self.client.force_authenticate(user=self.user)

        # Подписываемся
        response = self.client.post(self.subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_subscribed'])

        # Отписываемся
        response = self.client.post(self.subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['is_subscribed'])


# class DebugURLs(APITestCase):
#     """
#     Тест для проверки доступных URL.
#     """
#
#     def test_available_urls(self):
#         """Проверяем, какие URL доступны."""
#         print("\n=== Доступные URL ===")
#
#         try:
#             url = reverse('courses:lesson-list')
#             print(f"✅ lesson-list: {url}")
#         except Exception as e:
#             print(f"❌ lesson-list: {e}")
#
#         try:
#             url = reverse('lesson-detail', args=[1])
#             print(f"✅ lesson-detail: {url}")
#         except Exception as e:
#             print(f"❌ lesson-detail: {e}")
#
#         try:
#             url = reverse('course-list')
#             print(f"✅ course-list: {url}")
#         except Exception as e:
#             print(f"❌ course-list: {e}")
#
#         try:
#             url = reverse('course-detail', args=[1])
#             print(f"✅ course-detail: {url}")
#         except Exception as e:
#             print(f"❌ course-detail: {e}")
#
#         try:
#             url = reverse('course-subscription', args=[1])
#             print(f"✅ course-subscription: {url}")
#         except Exception as e:
#             print(f"❌ course-subscription: {e}")
#
#         try:
#             url = reverse('my-subscriptions')
#             print(f"✅ my-subscriptions: {url}")
#         except Exception as e:
#             print(f"❌ my-subscriptions: {e}")
#
#         print("=" * 40)
#
# # Запустите этот тест отдельно
# # python manage.py test courses.tests.DebugURLs -v 2