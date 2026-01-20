import stripe
from django.conf import settings
from django.core.exceptions import ValidationError

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name: str) -> str:
    """Создание продукта в Stripe"""
    try:
        product = stripe.Product.create(name=name)
        return product.id
    except stripe.error.StripeError as e:
        raise ValidationError(f"Ошибка создания продукта в Stripe: {str(e)}")


def create_stripe_price(product_id: str, amount: float) -> str:
    """Создание цены в Stripe (amount в рублях, конвертируется в копейки)"""
    try:
        price = stripe.Price.create(
            product=product_id,
            unit_amount=int(amount * 100),  # Конвертация в копейки
            currency='rub',
        )
        return price.id
    except stripe.error.StripeError as e:
        raise ValidationError(f"Ошибка создания цены в Stripe: {str(e)}")


def create_stripe_checkout_session(price_id: str, product_id: str) -> dict:
    """Создание сессии оплаты в Stripe"""
    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                'price': price_id,
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success/',
            cancel_url='http://localhost:8000/cancel/',
        )
        return {
            'session_id': session.id,
            'payment_link': session.url
        }
    except stripe.error.StripeError as e:
        raise ValidationError(f"Ошибка создания сессии в Stripe: {str(e)}")


def get_stripe_session_status(session_id: str) -> str:
    """Получение статуса сессии оплаты"""
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return session.payment_status
    except stripe.error.StripeError as e:
        raise ValidationError(f"Ошибка получения статуса сессии: {str(e)}")