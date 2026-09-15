"""Тексты экрана профиля пользователя."""


def get_screen_14_profile_text(full_name: str, client_avg, client_count: int,
                                executor_avg, executor_count: int) -> str:
    """Собирает карточку профиля с рейтингом отдельно за каждую роль."""

    client_line = f"Рейтинг: {client_avg} ({client_count} заказов)" if client_avg is not None else "Рейтинг: нет оценок"
    executor_line = (
        f"Рейтинг: {executor_avg} ({executor_count} заказов)" if executor_avg is not None else "Рейтинг: нет оценок"
    )
    return (
        "Профиль\n"
        f"{full_name}\n"
        "Как заказчик:\n"
        f"{client_line}\n"
        "Как исполнитель:\n"
        f"{executor_line}"
    )
