from celery import shared_task
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


@shared_task
def block_inactive_users():
    """
    Блокирует пользователей, которые не заходили более 30 дней.
    """
    # Дата месяц назад
    month_ago = timezone.now() - timedelta(days=30)

    # Находим пользователей, которые не заходили более месяца
    # Исключаем суперпользователей и администраторов
    users_to_block = User.objects.filter(
        is_active=True,
        last_login__lt=month_ago,
        is_superuser=False,
        is_staff=False
    )

    count = users_to_block.count()

    if count > 0:
        # Блокируем пользователей
        users_to_block.update(is_active=False)
        print(f"Заблокировано {count} неактивных пользователей")

    return f"Заблокировано {count} пользователей"