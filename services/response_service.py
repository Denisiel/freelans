"""Бизнес-операции отклика на заказ и выбора исполнителя."""

import datetime

from models.order import Order
from models.response import Response, ResponseStatus
from repositories.order_repository import select_order_by_id, update_order_deadline, update_order_status
from repositories.response_repository import (
    count_response_media,
    insert_response,
    insert_response_media,
    reject_other_responses,
    response_exists_for_order_and_executor,
    select_accepted_response,
    select_response_by_id,
    select_responses_by_executor,
    select_responses_by_order,
    update_response_status,
)


def validate_price(raw_value: str) -> float | None:
    """Проверяет цену отклика: положительное число."""

    try:
        value = float(raw_value.replace(",", "."))
    except (ValueError, AttributeError):
        return None
    if value <= 0:
        return None
    return value


def validate_comment(raw_text: str) -> str | None:
    """Проверяет необязательный комментарий: не длиннее 500 символов."""

    text = (raw_text or "").strip()
    if len(text) > 500:
        return None
    return text


def is_own_order(order: Order, executor_id: int) -> bool:
    """Проверяет, что исполнитель не пытается откликнуться на свой же заказ."""

    return order.client_id == executor_id


def has_already_responded(order_id: int, executor_id: int) -> bool:
    """Проверяет, откликался ли уже этот исполнитель на этот заказ."""

    return response_exists_for_order_and_executor(order_id, executor_id)


def submit_response(order_id: int, executor_id: int, price: float, comment: str | None = None,
                     media_file_ids: list | None = None) -> Response:
    """Сохраняет отклик исполнителя и прикреплённые к нему медиафайлы."""

    response = insert_response(order_id, executor_id, price, comment)
    for file_id in (media_file_ids or []):
        insert_response_media(response.id, file_id)
    return response


def get_responses_for_order(order_id: int) -> list[Response]:
    """Возвращает отклики на конкретный заказ."""

    return select_responses_by_order(order_id)


def get_my_responses(executor_id: int) -> list[Response]:
    """Возвращает отклики, оставленные пользователем как исполнителем."""

    return select_responses_by_executor(executor_id)


def get_response(response_id: int) -> Response | None:
    """Находит отклик по идентификатору."""

    return select_response_by_id(response_id)


def get_accepted_executor_response(order_id: int) -> Response | None:
    """Находит отклик выбранного исполнителя по заказу."""

    return select_accepted_response(order_id)


def count_media(response_id: int) -> int:
    """Считает количество медиафайлов, прикреплённых к отклику."""

    return count_response_media(response_id)


def choose_executor(order_id: int, response_id: int):
    """Подтверждает выбор исполнителя: заказ переходит в работу.

    Выбранный отклик получает статус ``accepted``, остальные — ``rejected``,
    а точный срок сдачи заказа отсчитывается от текущего момента.
    """

    order = select_order_by_id(order_id)

    update_response_status(response_id, ResponseStatus.ACCEPTED)
    reject_other_responses(order_id, keep_response_id=response_id)
    update_order_status(order_id, "in_progress")
    update_order_deadline(order_id, datetime.datetime.now() + datetime.timedelta(hours=order.deadline_hours))
