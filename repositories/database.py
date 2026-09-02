from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError

Base = declarative_base()


class DatabaseConnectionError(Exception):
    pass


class Database:
    def __init__(self, db_url: str):
        try:
            self._engine = create_engine(db_url, echo=False, future=True)
            self._session_factory = scoped_session(sessionmaker(bind=self._engine, expire_on_commit=False))
        except SQLAlchemyError as exc:
            raise DatabaseConnectionError(f"Не удалось создать подключение к БД: {exc}") from exc

    def create_all_tables(self):
        from models import user, category, order, response, response_media, review  # noqa: F401
        try:
            Base.metadata.create_all(self._engine)
        except SQLAlchemyError as exc:
            raise DatabaseConnectionError(f"Не удалось создать таблицы: {exc}") from exc

    def get_session(self):
        return self._session_factory()
