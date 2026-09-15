"""Тексты экрана ленты открытых заказов."""

from ui.screen_6_deadline.texts import get_deadline_hours_text


def get_screen_8_feed_text(index: int, total: int, category_name: str, description: str,
                            budget_rub: float, deadline_hours: int) -> str:
    """Формирует карточку одного открытого заказа с его порядковым номером."""

    return (
        f"Заказ {index} из {total}\n"
        f"Категория: {category_name}\n"
        f"Описание: {description}\n"
        f"Бюджет: {budget_rub:g} RUB\n"
        f"Срок: {get_deadline_hours_text(deadline_hours)}"
    )


NO_OPEN_ORDERS_TEXT = "Сейчас нет доступных заказов. Загляните позже."
END_OF_LIST_TEXT = "Больше заказов нет"
