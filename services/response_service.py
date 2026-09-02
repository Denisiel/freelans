from repositories.response_repository import ResponseRepository
from repositories.order_repository import OrderRepository
from models.response import ResponseStatus


class ResponseValidationError(Exception):
    pass


class ResponseService:
    def __init__(self, response_repo: ResponseRepository, order_repo: OrderRepository):
        self._response_repo = response_repo
        self._order_repo = order_repo

    def validate_price(self, raw_value: str) -> float:
        try:
            value = float(raw_value.replace(",", "."))
        except (ValueError, AttributeError):
            raise ResponseValidationError("Цена должна быть положительным числом.")
        if value <= 0:
            raise ResponseValidationError("Цена должна быть положительным числом.")
        return value

    def validate_comment(self, text: str) -> str:
        text = (text or "").strip()
        if len(text) > 500:
            raise ResponseValidationError(
                "Комментарий не должен превышать 500 символов. Сократите текст и попробуйте ещё раз."
            )
        return text

    def submit_response(self, order_id: int, executor_id: int, price: float, comment: str = None,
                         media_file_ids: list = None):
        order = self._order_repo.get_by_id(order_id)
        if order is None:
            raise ResponseValidationError("Заказ не найден.")
        if order.client_id == executor_id:
            raise ResponseValidationError("Нельзя откликнуться на свой заказ.")
        if self._response_repo.exists_for_order_and_executor(order_id, executor_id):
            raise ResponseValidationError("Вы уже откликались на этот заказ.")

        response = self._response_repo.create(order_id, executor_id, price, comment)
        for file_id in (media_file_ids or []):
            self._response_repo.add_media(response.id, file_id)
        return response

    def get_responses_for_order(self, order_id: int):
        return self._response_repo.get_by_order(order_id)

    def choose_executor(self, order_id: int, response_id: int):
        order = self._order_repo.get_by_id(order_id)
        if order is None or order.status != "open":
            raise ResponseValidationError("Этот заказ уже в работе или закрыт.")

        self._response_repo.update_status(response_id, ResponseStatus.ACCEPTED)
        self._response_repo.reject_all_except(order_id, keep_response_id=response_id)
        self._order_repo.update_status(order_id, "in_progress")
        return response_id
