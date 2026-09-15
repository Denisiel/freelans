"""SQLAlchemy-модель пользователя Telegram-бота."""

import datetime

from sqlalchemy import BigInteger, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from repositories.database import Base


class User(Base):
    """Один пользователь бота — может быть и заказчиком, и исполнителем."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    username: Mapped[str | None] = mapped_column(String(100), nullable=True)
    full_name: Mapped[str] = mapped_column(String(100), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )

    def __repr__(self):
        return f"<User id={self.id} telegram_id={self.telegram_id} full_name={self.full_name!r}>"
