#!/bin/bash

# Ждем готовности базы данных
echo "Waiting for database..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "Database started"

# Применяем миграции
echo "Applying migrations..."
python manage.py migrate --noinput

# Собираем статические файлы
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Создаем суперпользователя, если не существует (для продакшена лучше убрать)
echo "Creating superuser if not exists..."
python manage.py createsuperuser --noinput --username admin --email admin@example.com || true

exec "$@"