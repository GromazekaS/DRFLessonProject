from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import PaymentFilter


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet для платежей с поддержкой фильтрации и сортировки
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    # Подключаем фильтры
    filter_backends = [DjangoFilterBackend, OrderingFilter]

    # Поля для фильтрации (простые)
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']

    # Поля для сортировки
    ordering_fields = ['payment_date', 'amount']

    # Сортировка по умолчанию
    ordering = ['-payment_date']