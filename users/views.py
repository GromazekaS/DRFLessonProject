from django.db.models import Prefetch
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView

from .models import Payment, User
from courses.models import Course
from .serializers import PaymentSerializer, UserSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .filters import PaymentFilter
from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
# from django.contrib.auth.models import Group
from .serializers import UserSerializer, UserPublicSerializer
from .permissions import IsModerator, IsOwner  # Импортируем кастомные права
from .services.stripe import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_checkout_session,
    get_stripe_session_status
)


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet для работы с пользователями.
    """
    # queryset = User.objects.all()  # Не задаем здесь, переопределим get_queryset
    # serializer_class = UserSerializer  # Не задаем здесь, переопределим get_serializer_class
    permission_classes = [permissions.IsAuthenticated]  # По умолчанию требуем аутентификацию

    def get_permissions(self):
        """
        Кастомизация прав в зависимости от действия.
        """
        if self.action == 'create':
            # Для регистрации нового пользователя не требуем аутентификации
            return [permissions.AllowAny()]
        elif self.action == 'list':
            # Список пользователей - только для модераторов и админов
            return [permissions.IsAuthenticated(), IsModerator()]
        # Для остальных действий (retrieve, update, partial_update, destroy) используем стандартные
        return super().get_permissions()

    def get_queryset(self):
        """
        Возвращает разный queryset в зависимости от прав пользователя.
        """
        user = self.request.user
        if not user.is_authenticated:
            return User.objects.none()

        # Модераторы и админы видят всех пользователей
        if user.groups.filter(name='moderators').exists() or user.is_staff or user.is_superuser:
            return User.objects.prefetch_related('enrolled_courses', 'enrolled_lessons', 'payments').all()
        # Обычный пользователь видит только себя
        return User.objects.filter(id=user.id).prefetch_related('enrolled_courses', 'enrolled_lessons', 'payments')

    def get_serializer_class(self):
        """
        Выбирает сериализатор в зависимости от действия и прав.
        """
        user = self.request.user
        # Для списка (list) модераторы видят упрощенную версию
        if self.action == 'list' and (user.groups.filter(name='moderators').exists() or user.is_staff):
            return UserPublicSerializer  # Создадим сериализатор без чувствительных данных
        # Для детального просмотра себя или модератором - полная версия
        return UserSerializer

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """
        Эндпоинт для получения информации о текущем авторизованном пользователе.
        GET /api/users/me/
        """
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Переопределяем удаление: пользователь не может удалить себя через API.
        Удаление только для суперпользователя.
        """
        instance = self.get_object()
        if not request.user.is_superuser:
            return Response(
                {'detail': 'У вас нет прав на выполнение этого действия.'},
                status=status.HTTP_403_FORBIDDEN
            )
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


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


class UserRegistrationView(generics.CreateAPIView):
    """
    Эндпоинт для регистрации нового пользователя.
    POST /api/users/register/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer  # Используем полный сериализатор, т.к. в нем есть create
    permission_classes = [permissions.AllowAny]  # Доступно без аутентификации


class CreatePaymentView(APIView):
    """Создание платежа для курса"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        course_id = request.data.get('course_id')

        if not course_id:
            return Response({'error': 'course_id обязателен'}, status=400)

        course = get_object_or_404(Course, id=course_id)

        try:
            # 1. Создание продукта в Stripe
            product_id = create_stripe_product(course.title)

            # 2. Создание цены в Stripe
            price_id = create_stripe_price(product_id, float(course.price))

            # 3. Создание сессии оплаты
            session_data = create_stripe_checkout_session(price_id, product_id)

            # 4. Сохранение платежа в базе
            payment = Payment.objects.create(
                user=user,
                paid_course=course,
                amount=course.price,
                payment_method='stripe',
                stripe_product_id=product_id,
                stripe_price_id=price_id,
                stripe_session_id=session_data['session_id'],
                payment_link=session_data['payment_link'],
                status='pending'
            )

            return Response({
                'payment_id': payment.id,
                'payment_link': session_data['payment_link'],
                'status': 'pending'
            })

        except Exception as e:
            return Response({'error': str(e)}, status=400)

class PaymentStatusView(APIView):
    """Проверка статуса платежа"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, payment_id):
        payment = get_object_or_404(Payment, id=payment_id, user=request.user)

        try:
            status = get_stripe_session_status(payment.stripe_session_id)
            payment.status = status
            payment.save()

            return Response({
                'payment_id': payment.id,
                'status': status,
                'amount': payment.amount,
                'course': payment.paid_course.title if payment.paid_course else None
            })

        except Exception as e:
            return Response({'error': str(e)}, status=400)

class PaymentListView(generics.ListAPIView):
    """Список платежей пользователя"""
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-payment_date')

class PaymentSuccessAPIView(APIView):
    """API эндпоинт для успешной оплаты"""
    permission_classes = []  # Доступ без аутентификации

    def get(self, request):
        return Response({
            'status': 'success',
            'message': 'Платеж успешно завершен. Спасибо за покупку!',
            'instruction': 'Вы можете проверить статус платежа в личном кабинете'
        })

class PaymentCancelAPIView(APIView):
    """API эндпоинт для отмены оплаты"""
    permission_classes = []  # Доступ без аутентификации

    def get(self, request):
        return Response({
            'status': 'canceled',
            'message': 'Платеж был отменен',
            'instruction': 'Вы можете повторить оплату в любое время'
        })