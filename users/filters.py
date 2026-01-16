import django_filters
from django_filters import rest_framework as filters
from .models import Payment


class PaymentFilter(filters.FilterSet):
    # Фильтрация по курсу (по ID курса)
    paid_course = filters.NumberFilter(
        field_name='paid_course__id',
        label='ID курса'
    )

    # Фильтрация по названию курса
    paid_course_title = filters.CharFilter(
        field_name='paid_course__title',
        lookup_expr='icontains',
        label='Название курса содержит'
    )

    # Фильтрация по уроку (по ID урока)
    paid_lesson = filters.NumberFilter(
        field_name='paid_lesson__id',
        label='ID урока'
    )

    # Фильтрация по названию урока
    paid_lesson_title = filters.CharFilter(
        field_name='paid_lesson__title',
        lookup_expr='icontains',
        label='Название урока содержит'
    )

    # Фильтрация по способу оплаты
    payment_method = filters.ChoiceFilter(
        choices=Payment.PAYMENT_METHOD_CHOICES,
        label='Способ оплаты'
    )

    # Фильтрация по дате (диапазон дат)
    payment_date_from = filters.DateFilter(
        field_name='payment_date',
        lookup_expr='gte',
        label='Дата оплаты с'
    )

    payment_date_to = filters.DateFilter(
        field_name='payment_date',
        lookup_expr='lte',
        label='Дата оплаты по'
    )

    # Сортировка по дате оплаты (возможность указать порядок)
    ordering = filters.OrderingFilter(
        fields=(
            ('payment_date', 'date'),
            ('amount', 'amount'),
        ),
        field_labels={
            'payment_date': 'Дата оплаты',
            'amount': 'Сумма',
        }
    )

    class Meta:
        model = Payment
        fields = [
            'paid_course',
            'paid_lesson',
            'payment_method',
            'payment_date_from',
            'payment_date_to',
        ]