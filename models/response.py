from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Numeric
from repositories.database import Base


class ResponseStatus:
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Response(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    executor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    price = Column(Numeric(12, 2), nullable=False)
    comment = Column(String(500), nullable=True)
    status = Column(String(20), nullable=False, default=ResponseStatus.PENDING)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<Response id={self.id} order_id={self.order_id} status={self.status}>"
