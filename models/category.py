"""SQLAlchemy-модель справочника категорий заказов."""

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from repositories.database import Base


class Category(Base):
    """Одна категория, которую заказчик выбирает при создании заказа."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)

    def __repr__(self):
        return f"<Category id={self.id} name={self.name!r}>"
