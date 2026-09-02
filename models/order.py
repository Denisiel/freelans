from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from repositories.database import Base


class OrderStatus:
    OPEN = "open"
    IN_PROGRESS = "in_progress"
    DISPUTED = "disputed"
    COMPLETED = "completed"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    description = Column(String(1000), nullable=False)
    budget = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(3), nullable=False, default="RUB")
    budget_rub = Column(Numeric(12, 2), nullable=False)
    deadline = Column(DateTime, nullable=False)
    status = Column(String(20), nullable=False, default=OrderStatus.OPEN)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Order id={self.id} status={self.status} budget_rub={self.budget_rub}>"
