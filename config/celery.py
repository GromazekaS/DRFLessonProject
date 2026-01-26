from __future__ import absolute_import, unicode_literals
import os

# Определяем, запущены ли мы в режиме Celery worker
# Простой способ: проверяем аргументы командной строки
import sys
if 'celery' in sys.argv[0] or 'worker' in sys.argv:
    from eventlet import monkey_patch
    monkey_patch()
    print("Eventlet monkey patch applied for Celery worker.")

# Теперь можно импортировать остальное
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    # Блокировка неактивных пользователей каждый день в 2:00
    'block-inactive-users': {
        'task': 'users.tasks.block_inactive_users',
        'schedule': crontab(hour=2, minute=0),  # Каждый день в 2:00
    },
}