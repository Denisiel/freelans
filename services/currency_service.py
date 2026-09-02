from api.currency_api import CurrencyApiClient, CurrencyApiError


class CurrencyConversionError(Exception):
    pass


class CurrencyService:
    def __init__(self, api_client: CurrencyApiClient):
        self._api_client = api_client

    def convert_to_rub(self, amount: float, currency_code: str) -> float:
        try:
            rate = self._api_client.get_rate_to_rub(currency_code)
        except CurrencyApiError as exc:
            raise CurrencyConversionError(
                "Не удалось получить курс валют. Попробуйте позже или укажите бюджет в рублях."
            ) from exc
        return round(amount * rate, 2)
