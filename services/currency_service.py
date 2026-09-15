"""Пересчёт бюджета заказа в рубли через внешний API курса валют."""

from api.currency_api import get_rate_to_rub


def convert_to_rub(amount: float, currency_code: str) -> float:
    """Пересчитывает сумму в валюте в рубли по текущему курсу.

    Сетевые ошибки API намеренно не перехватываются здесь: их обрабатывает
    вызывающий код UI-слоя, который покажет пользователю понятное сообщение.
    """

    rate = get_rate_to_rub(currency_code)
    return round(amount * rate, 2)
