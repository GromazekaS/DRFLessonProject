FROM python:3.13-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем зависимости системы
RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей в контейнер
COPY requirements.txt ./

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код приложения в контейнер
COPY . .

# Определяем переменные окружения
ENV SECRET_KEY="django-insecure-cdi9^jjp5)dlgm5(xaqp0ts5a6!cs+loxii)(pjyr8eu(iw9&x"
ENV CELERY_BROKER_URL="redis://redis:6379/0"
ENV CELERY_BACKEND="redis://redis:6379/0"

# Создаем директорию для медиафайлов
RUN mkdir -p /app/media
RUN mkdir -p /app/static

# Пробрасываем порт, который будет использовать Django
EXPOSE 8000

# Команда для запуска приложения
CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]