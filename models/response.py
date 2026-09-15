"""SQLAlchemy-модель отклика исполнителя на заказ."""

import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from repositories.database import Base


class ResponseStatus:
    """Допустимые значения статуса отклика."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Response(Base):
    """Предложение исполнителя выполнить конкретный заказ за свою цену."""

    __tablename__ = "responses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    executor_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    price: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    comment: Mapped[str | None] = mapped_column(String(500), nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=ResponseStatus.PENDING)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )

    def __repr__(self):
        return f"<Response id={self.id} order_id={self.order_id} status={self.status}>"
