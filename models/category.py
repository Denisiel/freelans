from sqlalchemy import Column, Integer, String
from repositories.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Category id={self.id} name={self.name!r}>"
