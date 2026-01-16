from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватарка')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    # Способы оплаты
    CASH = 'cash'
    TRANSFER = 'transfer'

    PAYMENT_METHOD_CHOICES = [
        (CASH, 'Наличные'),
        (TRANSFER, 'Перевод на счет'),
    ]

    # Основные поля
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Пользователь'
    )

    payment_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата оплаты'
    )

    paid_course = models.ForeignKey(
        'courses.Course',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Оплаченный курс'
    )

    paid_lesson = models.ForeignKey(
        'courses.Lesson',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='payments',
        verbose_name='Оплаченный урок'
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Сумма оплаты'
    )

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        verbose_name='Способ оплаты'
    )

    class Meta:
        verbose_name = 'Платеж'
        verbose_name_plural = 'Платежи'
        ordering = ['-payment_date']  # Сортировка по дате (новые первые)

    def __str__(self):
        return f"{self.payment_date} - {self.user.email} - {self.amount} - {self.payment_method}"