"""Бизнес-операции, связанные с пользователем бота."""

from models.user import User
from repositories.user_repository import get_or_create_user, select_user_by_id, select_user_by_telegram_id


def register_or_get_user(telegram_id: int, username: str | None, full_name: str) -> User:
    """Возвращает существующего пользователя либо регистрирует нового."""

    return get_or_create_user(telegram_id, username, full_name)


def get_user_by_telegram_id(telegram_id: int) -> User | None:
    """Находит пользователя по Telegram ID, если он уже писал боту."""

    return select_user_by_telegram_id(telegram_id)


def get_user_by_id(user_id: int) -> User | None:
    """Находит пользователя по внутреннему идентификатору таблицы."""

    return select_user_by_id(user_id)
