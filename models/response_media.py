from sqlalchemy import Column, Integer, String, ForeignKey
from repositories.database import Base


class ResponseMedia(Base):
    __tablename__ = "response_media"

    id = Column(Integer, primary_key=True, autoincrement=True)
    response_id = Column(Integer, ForeignKey("responses.id"), nullable=False)
    telegram_file_id = Column(String(200), nullable=False)

    def __repr__(self):
        return f"<ResponseMedia id={self.id} response_id={self.response_id}>"
