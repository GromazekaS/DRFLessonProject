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
    filterset_class = PaymentFilter

    # Поля, по которым возможна сортировка
    ordering_fields = ['payment_date', 'amount']

    # Сортировка по умолчанию (последние платежи сначала)
    ordering = ['-payment_date']

    def get_queryset(self):
        """
        Дополнительная фильтрация (например, по текущему пользователю)
        """
        queryset = super().get_queryset()

        # Пример: фильтрация только платежей текущего пользователя
        # if self.request.user.is_authenticated:
        #     queryset = queryset.filter(user=self.request.user)

        return queryset