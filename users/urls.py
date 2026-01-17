from django.urls import path
from .views import PaymentViewSet
from rest_framework.routers import DefaultRouter

app_name = 'users'  # Пространство имен приложения

router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [

              ] + router.urls