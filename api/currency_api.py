"""Функции для получения курса валют через сервис currencyapi.com.

Модуль относится к слою внешних API: он формирует HTTP-запрос, проверяет ответ
сервера и возвращает готовое число. Остальные части приложения благодаря этому
не зависят от формата ответа currencyapi.com.
"""

import requests

import config


def get_rate_to_rub(currency_code: str) -> float:
    """Возвращает курс: сколько рублей стоит 1 единица валюты.

    Для рубля курс всегда равен единице, и сеть при этом не используется.
    Сетевые и HTTP-ошибки, а также отсутствие нужной валюты в ответе,
    намеренно не перехватываются: их обрабатывает сервисный слой, который
    превращает их в понятное пользователю сообщение об ошибке.
    """

    if currency_code.upper() == "RUB":
        return 1.0

    response = requests.get(
        config.CURRENCY_API_URL,
        params={
            "apikey": config.CURRENCY_API_KEY,
            "base_currency": currency_code.upper(),
            "currencies": "RUB",
        },
        timeout=5,
    )
    response.raise_for_status()

    # В ключе data лежит курс запрошенной валюты к рублю.
    rate = response.json()["data"]["RUB"]["value"]
    return float(rate)
