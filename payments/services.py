import stripe
from django.conf import settings


stripe.api_key = settings.STRIPE_API_KEY


def create_stripe_price(product, price):
    """ Создает stripe цену на продукт и возвращает ее. """
    try:
        price = stripe.Price.create(
            currency="usd",
            unit_amount=price,
            recurring={"interval": "month"},
            product_data={"name": product},
        )
        price_id = price.id
    except Exception as e:
        return f"Ошибка создания стоимости: {str(e)}."
    else:
        return price_id


def create_stripe_session(price):
    """ Создает stripe сессию и возвращает ссылку на оплату. """
    try:
        session = stripe.checkout.Session.create(
            success_url="https://example.com/success",
            line_items=[{"price": price, "quantity": 1}],
            mode="subscription",
        )
        session_url = session.url
    except Exception as e:
        return f"Ошибка создания платежа: {str(e)}."
    else:
        return session_url
