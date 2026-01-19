from django.urls import path
from .views import PaymentViewSet, UserViewSet
from rest_framework.routers import DefaultRouter

app_name = 'users'  # Пространство имен приложения

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'users', UserViewSet, basename='users')

urlpatterns = [

              ] + router.urls