"""Операции чтения справочника категорий заказов."""

from sqlalchemy import select

from models.category import Category
from repositories.database import get_session


def select_all_categories() -> list[Category]:
    """Возвращает все категории из справочника."""

    with get_session() as session:
        return list(session.scalars(select(Category)))


def select_category_by_id(category_id: int) -> Category | None:
    """Находит категорию по идентификатору либо возвращает ``None``."""

    with get_session() as session:
        return session.get(Category, category_id)


def insert_default_categories():
    """Заполняет справочник стандартными категориями, если он ещё пуст."""

    default_names = ["Дизайн", "Разработка", "Копирайтинг", "Маркетинг", "Другое"]

    with get_session() as session:
        # Повторный запуск бота не должен дублировать категории.
        already_exists = session.scalar(select(Category).limit(1)) is not None
        if already_exists:
            return

        for name in default_names:
            session.add(Category(name=name))
        session.commit()
