from django.urls import path
from .views import (UserViewSet, UserRegistrationView,
                    PaymentViewSet, PaymentStatusView, PaymentListView, CreatePaymentView,
                    PaymentSuccessAPIView, PaymentCancelAPIView,
                    )
from rest_framework.routers import DefaultRouter

app_name = 'users'  # Пространство имен приложения

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='user-register'),

    path('payments/', PaymentListView.as_view(), name='payment-list'),
    path('payments/create/', CreatePaymentView.as_view(), name='payment-create'),
    path('payments/<int:payment_id>/status/', PaymentStatusView.as_view(), name='payment-status'),
    path('success/', PaymentSuccessAPIView.as_view(), name='payment-success'),
    path('cancel/', PaymentCancelAPIView.as_view(), name='payment-cancel'),
] + router.urls