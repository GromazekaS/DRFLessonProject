from django.db.models import Prefetch
from rest_framework import viewsets
from .models import Payment, User
from courses.models import Course
from .serializers import PaymentSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import PaymentFilter


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        # Оптимизация запросов для избежания N+1
        return User.objects.prefetch_related(
            Prefetch(
                'enrolled_courses',
                queryset=Course.objects.prefetch_related('lessons')
            ),
            'enrolled_lessons',
            'payments'
        ).all()

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