"""Тексты экрана подтверждения и публикации заказа."""

from ui.screen_6_deadline.texts import get_deadline_hours_text


def get_screen_7_confirm_text(category_name: str, description: str, budget: float,
                               currency: str, deadline_hours: int) -> str:
    """Собирает итоговую карточку заказа для проверки перед публикацией."""

    return (
        "Проверьте заказ перед публикацией\n"
        f"Категория: {category_name}\n"
        f"Описание: {description}\n"
        f"Бюджет: {budget:g} {currency}\n"
        f"Срок: {get_deadline_hours_text(deadline_hours)}"
    )


ORDER_PUBLISHED_TEXT = "Заказ опубликован."
