import requests


class CurrencyApiError(Exception):
    pass


class CurrencyApiClient:
    def __init__(self, api_key: str, base_url: str, timeout: int = 5):
        self._api_key = api_key
        self._base_url = base_url
        self._timeout = timeout

    def get_rate_to_rub(self, currency_code: str) -> float:
        if currency_code.upper() == "RUB":
            return 1.0

        params = {
            "apikey": self._api_key,
            "base_currency": currency_code.upper(),
            "currencies": "RUB",
        }
        try:
            resp = requests.get(self._base_url, params=params, timeout=self._timeout)
            resp.raise_for_status()
            payload = resp.json()
        except requests.RequestException as exc:
            raise CurrencyApiError(f"Сервис курса валют недоступен: {exc}") from exc
        except ValueError as exc:
            raise CurrencyApiError(f"Некорректный ответ сервиса курса валют: {exc}") from exc

        try:
            rate = payload["data"]["RUB"]["value"]
            return float(rate)
        except (KeyError, TypeError, ValueError) as exc:
            raise CurrencyApiError(f"В ответе сервиса нет курса для {currency_code}: {exc}") from exc
