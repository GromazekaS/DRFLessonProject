import django_filters
from django_filters import rest_framework as filters
from .models import Payment


class PaymentFilter(filters.FilterSet):
    # Простые фильтры без сложной логики
    paid_course = filters.NumberFilter(field_name='paid_course__id')
    paid_lesson = filters.NumberFilter(field_name='paid_lesson__id')
    payment_method = filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ['paid_course', 'paid_lesson', 'payment_method']