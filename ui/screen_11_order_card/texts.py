"""Тексты экрана карточки заказа."""

from ui.screen_10_my_orders.texts import get_status_label
from ui.screen_6_deadline.texts import get_deadline_display_text


def get_screen_11_order_card_text(category_name: str, description: str, budget_rub: float,
                                   deadline, deadline_hours: int, status: str) -> str:
    """Собирает подробную карточку одного заказа."""

    return (
        "Карточка заказа\n"
        f"Категория: {category_name}\n"
        f"Описание: {description}\n"
        f"Бюджет: {budget_rub:g} RUB\n"
        f"Срок: {get_deadline_display_text(deadline, deadline_hours)}\n"
        f"Статус: {get_status_label(status)}"
    )


UNDER_DEVELOPMENT_TEXT = "Этот раздел ещё в разработке. Скоро будет доступен."
