"""Бизнес-операции создания заказа, ленты и карточек заказов."""

from models.category import Category
from models.order import Order, OrderStatus
from repositories.category_repository import select_all_categories, select_category_by_id
from repositories.order_repository import (
    insert_order,
    select_open_orders,
    select_order_by_id,
    select_orders_by_client,
    update_order_status,
)
from services.currency_service import convert_to_rub


def get_categories() -> list[Category]:
    """Возвращает справочник категорий для экрана выбора."""

    return select_all_categories()


def get_category(category_id: int) -> Category | None:
    """Находит категорию по идентификатору."""

    return select_category_by_id(category_id)


def validate_description(text: str) -> str | None:
    """Проверяет описание заказа: от 1 до 1000 символов.

    Возвращает очищенный от пробелов текст либо ``None`` при некорректном вводе.
    """

    text = (text or "").strip()
    if not text or len(text) > 1000:
        return None
    return text


def validate_budget(raw_value: str) -> float | None:
    """Проверяет введённый бюджет: положительное число.

    Возвращает число либо ``None``, если строку не удалось разобрать.
    """

    try:
        value = float(raw_value.replace(",", "."))
    except (ValueError, AttributeError):
        return None
    if value <= 0:
        return None
    return value


def validate_deadline_hours(raw_value: str) -> int | None:
    """Проверяет введённый срок в часах: положительное целое число."""

    try:
        hours = int(raw_value.strip())
    except (ValueError, AttributeError):
        return None
    if hours <= 0:
        return None
    return hours


def calculate_budget_rub(budget: float, currency: str) -> float:
    """Пересчитывает бюджет в рубли через сервис валют.

    Ошибки внешнего API намеренно не перехватываются: их обрабатывает
    вызывающий код UI-слоя.
    """

    return convert_to_rub(budget, currency)


def publish_order(client_id: int, category_id: int, description: str, budget: float,
                   currency: str, budget_rub: float, deadline_hours: int) -> Order:
    """Публикует заказ со статусом ``open``."""

    return insert_order(client_id, category_id, description, budget, currency, budget_rub, deadline_hours)


def get_feed(viewer_client_id: int) -> list[Order]:
    """Возвращает открытые заказы для ленты, кроме заказов самого пользователя."""

    return select_open_orders(exclude_client_id=viewer_client_id)


def get_my_orders(client_id: int) -> list[Order]:
    """Возвращает заказы, опубликованные пользователем как заказчиком."""

    return select_orders_by_client(client_id)


def get_order(order_id: int) -> Order | None:
    """Находит заказ по идентификатору."""

    return select_order_by_id(order_id)


def mark_disputed(order_id: int):
    """Переводит заказ в статус спора."""

    return update_order_status(order_id, OrderStatus.DISPUTED)


def mark_completed(order_id: int):
    """Переводит заказ в статус завершённого."""

    return update_order_status(order_id, OrderStatus.COMPLETED)
