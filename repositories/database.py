"""Настройка подключения к базе данных."""

import sqlalchemy
from sqlalchemy.orm import DeclarativeBase, sessionmaker

import config

# pool_pre_ping проверяет соединение перед выдачей из пула и помогает пережить
# разрыв простаивавшего подключения к БД.
engine = sqlalchemy.create_engine(config.DATABASE_URL, echo=False, pool_pre_ping=True)


class Base(DeclarativeBase):
    """Общий базовый класс всех таблиц SQLAlchemy."""


# Фабрика создаёт отдельную сессию для каждой операции репозитория.
get_session = sessionmaker(bind=engine, expire_on_commit=False)


def create_all_tables():
    """Создаёт все таблицы проекта, если их ещё нет."""

    # Импорт моделей внутри функции нужен, чтобы их классы успели
    # зарегистрироваться в Base.metadata до вызова create_all.
    from models import user, category, order, response, response_media, review  # noqa: F401

    Base.metadata.create_all(engine)
