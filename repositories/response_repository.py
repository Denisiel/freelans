from models.response import Response, ResponseStatus
from models.response_media import ResponseMedia


class ResponseRepository:
    def __init__(self, session):
        self._session = session

    def create(self, order_id: int, executor_id: int, price: float, comment: str = None) -> Response:
        response = Response(
            order_id=order_id,
            executor_id=executor_id,
            price=price,
            comment=comment,
            status=ResponseStatus.PENDING,
        )
        self._session.add(response)
        self._session.commit()
        return response

    def add_media(self, response_id: int, telegram_file_id: str) -> ResponseMedia:
        media = ResponseMedia(response_id=response_id, telegram_file_id=telegram_file_id)
        self._session.add(media)
        self._session.commit()
        return media

    def get_by_id(self, response_id: int):
        return self._session.query(Response).filter_by(id=response_id).first()

    def get_by_order(self, order_id: int):
        return (
            self._session.query(Response)
            .filter_by(order_id=order_id)
            .order_by(Response.created_at.desc())
            .all()
        )

    def exists_for_order_and_executor(self, order_id: int, executor_id: int) -> bool:
        return (
            self._session.query(Response)
            .filter_by(order_id=order_id, executor_id=executor_id)
            .first()
            is not None
        )

    def update_status(self, response_id: int, status: str):
        response = self.get_by_id(response_id)
        if response is None:
            return None
        response.status = status
        self._session.commit()
        return response

    def reject_all_except(self, order_id: int, keep_response_id: int):
        others = (
            self._session.query(Response)
            .filter(Response.order_id == order_id, Response.id != keep_response_id)
            .all()
        )
        for r in others:
            r.status = ResponseStatus.REJECTED
        self._session.commit()
