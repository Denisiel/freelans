"""SQLAlchemy-модель заказа."""

import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from repositories.database import Base


class OrderStatus:
    """Допустимые значения статуса заказа."""

    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DISPUTED = "disputed"
    COMPLETED = "completed"


class Order(Base):
    """Заказ, опубликованный заказчиком, со всеми условиями и статусом."""

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    client_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("categories.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(1000), nullable=False)
    budget: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="RUB")
    budget_rub: Mapped[float] = mapped_column(Numeric(12, 2), nullable=False)
    # Отсчёт срока начинается не при публикации, а с момента выбора исполнителя,
    # поэтому храним длительность в часах и точную дату отдельно.
    deadline_hours: Mapped[int] = mapped_column(Integer, nullable=False)
    deadline: Mapped[datetime.datetime | None] = mapped_column(DateTime, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default=OrderStatus.OPEN)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )

    def __repr__(self):
        return f"<Order id={self.id} status={self.status} budget_rub={self.budget_rub}>"
