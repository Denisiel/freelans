"""Тексты экрана списка собственных заказов и откликов."""

STATUS_LABELS = {
    "open": "Открыт",
    "in_progress": "В работе",
    "disputed": "Спор",
    "completed": "Завершён",
}


def get_status_label(status: str) -> str:
    """Переводит статус заказа из кода БД в текст для пользователя."""

    return STATUS_LABELS.get(status, status)


def get_screen_10_my_orders_text(index: int, total: int, role_text: str, category_name: str,
                                  status_text: str, budget_rub: float) -> str:
    """Формирует карточку одного заказа или отклика в списке «Мои заказы»."""

    return (
        f"Заказ {index} из {total}\n"
        f"Роль: {role_text}\n"
        f"Категория: {category_name}\n"
        f"Статус: {status_text}\n"
        f"Бюджет: {budget_rub:g} RUB"
    )


NO_MY_ORDERS_TEXT = "У вас пока нет заказов или откликов. Начните с ленты заказов или создайте свой."
