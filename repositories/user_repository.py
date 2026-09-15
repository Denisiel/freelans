"""Операции чтения и записи пользователей бота."""

from sqlalchemy import select

from models.user import User
from repositories.database import get_session


def select_user_by_telegram_id(telegram_id: int) -> User | None:
    """Находит пользователя по его Telegram ID."""

    with get_session() as session:
        return session.scalar(select(User).where(User.telegram_id == telegram_id))


def select_user_by_id(user_id: int) -> User | None:
    """Находит пользователя по внутреннему идентификатору таблицы."""

    with get_session() as session:
        return session.get(User, user_id)


def insert_user(telegram_id: int, username: str | None, full_name: str) -> User:
    """Создаёт нового пользователя при первом обращении к боту."""

    with get_session() as session:
        user = User(telegram_id=telegram_id, username=username, full_name=full_name)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def get_or_create_user(telegram_id: int, username: str | None, full_name: str) -> User:
    """Возвращает существующего пользователя либо создаёт нового."""

    user = select_user_by_telegram_id(telegram_id)
    if user is not None:
        return user
    return insert_user(telegram_id, username, full_name)
