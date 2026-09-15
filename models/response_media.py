"""SQLAlchemy-модель медиафайла, прикреплённого к отклику."""

from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from repositories.database import Base


class ResponseMedia(Base):
    """Один файл (фото или документ), прикреплённый к отклику исполнителя."""

    __tablename__ = "response_media"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    response_id: Mapped[int] = mapped_column(Integer, ForeignKey("responses.id"), nullable=False)
    telegram_file_id: Mapped[str] = mapped_column(String(200), nullable=False)

    def __repr__(self):
        return f"<ResponseMedia id={self.id} response_id={self.response_id}>"
