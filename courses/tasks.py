from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Course, Subscription
import time

User = get_user_model()


@shared_task
def send_course_update_notifications_detailed(course_id, changed_fields=None, updated_by=None):
    """Детальная рассылка уведомлений с информацией об изменениях"""
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()

        course = Course.objects.get(id=course_id)
        subscriptions = course.subscription_set.all()  # Предполагаем related_name='subscription_set'

        if not subscriptions.exists():
            print(f"У курса '{course.title}' нет подписчиков")
            return {'status': 'no_subscribers'}

        # Получаем информацию о том, кто обновил курс
        updated_by_user = None
        if updated_by:
            try:
                updated_by_user = User.objects.get(id=updated_by)
            except User.DoesNotExist:
                pass

        # Имитация отправки писем
        for subscription in subscriptions:
            user = subscription.user
            if user.email:
                print(f"=== Уведомление отправлено ===")
                print(f"Кому: {user.email}")
                print(f"Тема: Обновление курса '{course.title}'")

                if changed_fields:
                    print(f"Изменены поля: {', '.join(changed_fields)}")

                if updated_by_user:
                    print(f"Обновил: {updated_by_user.get_full_name() or updated_by_user.email}")

                print(f"Ссылка на курс: /courses/{course.id}/")
                print("---")

        return {
            'status': 'success',
            'course_id': course_id,
            'subscribers_notified': subscriptions.count()
        }

    except Course.DoesNotExist:
        return {'status': 'error', 'message': 'Курс не найден'}