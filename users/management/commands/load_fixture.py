# users/management/commands/load_fixture.py
import os
from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings


class Command(BaseCommand):
    help = 'Загружает фикстуру с тестовыми данными из JSON файла'

    def add_arguments(self, parser):
        parser.add_argument(
            '--flush',
            action='store_true',
            help='Удалить существующие данные перед загрузкой фикстуры'
        )
        parser.add_argument(
            '--fixture',
            type=str,
            default='initial_fixture.json',
            help='Имя файла фикстуры (по умолчанию: initial_fixture.json)'
        )

    def handle(self, *args, **options):
        fixture_name = options['fixture']

        # Путь к фикстуре
        fixture_path = os.path.join(settings.BASE_DIR, 'users', 'fixtures', fixture_name)

        # Проверяем существование файла
        if not os.path.exists(fixture_path):
            raise CommandError(f'❌ Файл фикстуры не найден: {fixture_path}')

        self.stdout.write(f'📂 Файл фикстуры: {fixture_path}')

        # Очистка данных, если указан флаг --flush
        if options['flush']:
            self.stdout.write('🗑️  Очистка существующих данных...')
            self.flush_data()

        # Загрузка фикстуры
        self.stdout.write('⬆️  Загрузка фикстуры...')

        try:
            # Используем стандартную команду loaddata с детальным выводом
            call_command('loaddata', fixture_path, verbosity=2)
            self.stdout.write(self.style.SUCCESS('✅ Фикстура успешно загружена!'))

            # Показываем статистику
            self.show_statistics()

        except Exception as e:
            self.stdout.write(self.style.ERROR('❌ Ошибка при загрузке фикстуры!'))
            self.stdout.write(f'Подробности: {e}')

            # Предлагаем диагностику
            self.stdout.write("\n📋 Попробуйте:")
            self.stdout.write(f'1. Проверить JSON: python -m json.tool {fixture_path}')
            self.stdout.write(f'2. Загрузить с детализацией: python manage.py loaddata {fixture_name} --verbosity 3')
            self.stdout.write(f'3. Создать тестовую фикстуру: python manage.py create_test_fixture')

    def flush_data(self):
        """Очистка данных"""
        try:
            from users.models import Payment
            from courses.models import Lesson, Course
            from django.contrib.auth import get_user_model

            User = get_user_model()

            # Удаляем в правильном порядке (сначала платежи, потом уроки, курсы, пользователи)
            Payment.objects.all().delete()
            self.stdout.write('  ✓ Очищена таблица платежей')

            Lesson.objects.all().delete()
            self.stdout.write('  ✓ Очищена таблица уроков')

            Course.objects.all().delete()
            self.stdout.write('  ✓ Очищена таблица курсов')

            # Удаляем только обычных пользователей, оставляем суперпользователей
            User.objects.filter(is_superuser=False).delete()
            self.stdout.write('  ✓ Очищена таблица пользователей')

        except Exception as e:
            raise CommandError(f'Ошибка при очистке данных: {e}')

    def show_statistics(self):
        """Показывает статистику загруженных данных"""
        try:
            from users.models import User, Payment
            from courses.models import Course, Lesson

            self.stdout.write("\n📊 СТАТИСТИКА:")
            self.stdout.write("=" * 30)
            self.stdout.write(f"Пользователей: {User.objects.count()}")
            self.stdout.write(f"Курсов: {Course.objects.count()}")
            self.stdout.write(f"Уроков: {Lesson.objects.count()}")
            self.stdout.write(f"Платежей: {Payment.objects.count()}")

        except Exception as e:
            self.stdout.write(f"⚠ Не удалось получить статистику: {e}")