"""SQLAlchemy-модель взаимной оценки заказчика и исполнителя."""

import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from repositories.database import Base


class Review(Base):
    """Оценка (1-5 звёзд) и комментарий, оставленные после завершения заказа."""

    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    order_id: Mapped[int] = mapped_column(Integer, ForeignKey("orders.id"), nullable=False)
    from_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    to_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    rating: Mapped[int] = mapped_column(Integer, nullable=False)
    comment: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime, default=lambda: datetime.datetime.now(datetime.timezone.utc), nullable=False
    )

    def __repr__(self):
        return f"<Review id={self.id} order_id={self.order_id} rating={self.rating}>"
