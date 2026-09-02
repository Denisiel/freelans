from datetime import datetime, timezone
from sqlalchemy import Column, Integer, BigInteger, String, DateTime
from repositories.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger, unique=True, nullable=False)
    username = Column(String(100), nullable=True)
    full_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    def __repr__(self):
        return f"<User id={self.id} telegram_id={self.telegram_id} full_name={self.full_name!r}>"
