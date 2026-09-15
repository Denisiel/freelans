"""Тексты экрана отклика на заказ и его подэкранов."""


def get_screen_9_response_menu_text(price_text: str, comment_text: str, media_count: int) -> str:
    """Показывает текущее состояние черновика отклика."""

    return (
        "Отклик на заказ\n"
        f"Цена: {price_text}\n"
        f"Комментарий: {comment_text}\n"
        f"Медиафайлы: {media_count} прикреплено"
    )


RESPONSE_SENT_TEXT = "Отклик отправлен."
NEED_PRICE_FIRST_TEXT = "Сначала укажите цену."
CANNOT_RESPOND_OWN_ORDER_TEXT = "Нельзя откликнуться на свой заказ."
ALREADY_RESPONDED_TEXT = "Вы уже откликались на этот заказ."

ASK_PRICE_TEXT = "Укажите вашу цену за выполнение заказа"
PRICE_INVALID_TEXT = "Цена должна быть положительным числом."

ASK_COMMENT_TEXT = "Добавьте комментарий к отклику\nНеобязательно, до 500 символов"
COMMENT_TOO_LONG_TEXT = "Комментарий не должен превышать 500 символов. Сократите текст и попробуйте ещё раз."

ASK_MEDIA_TEXT = "Прикрепите медиафайлы\nОтправьте одно или несколько изображений/файлов"
