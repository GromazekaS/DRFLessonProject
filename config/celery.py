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

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()