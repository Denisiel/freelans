"""Операции чтения и записи откликов на заказы и их медиафайлов."""

from sqlalchemy import select

from models.response import Response, ResponseStatus
from models.response_media import ResponseMedia
from repositories.database import get_session


def insert_response(order_id: int, executor_id: int, price: float, comment: str | None = None) -> Response:
    """Сохраняет новый отклик исполнителя со статусом ``pending``."""

    with get_session() as session:
        response = Response(
            order_id=order_id,
            executor_id=executor_id,
            price=price,
            comment=comment,
            status=ResponseStatus.PENDING,
        )
        session.add(response)
        session.commit()
        session.refresh(response)
        return response


def insert_response_media(response_id: int, telegram_file_id: str) -> ResponseMedia:
    """Добавляет медиафайл к отклику."""

    with get_session() as session:
        media = ResponseMedia(response_id=response_id, telegram_file_id=telegram_file_id)
        session.add(media)
        session.commit()
        return media


def select_response_by_id(response_id: int) -> Response | None:
    """Находит отклик по идентификатору."""

    with get_session() as session:
        return session.get(Response, response_id)


def select_responses_by_order(order_id: int) -> list[Response]:
    """Возвращает отклики на конкретный заказ, новые сверху."""

    with get_session() as session:
        query = select(Response).where(Response.order_id == order_id).order_by(Response.created_at.desc())
        return list(session.scalars(query))


def select_responses_by_executor(executor_id: int) -> list[Response]:
    """Возвращает отклики, оставленные конкретным исполнителем."""

    with get_session() as session:
        query = select(Response).where(Response.executor_id == executor_id).order_by(Response.created_at.desc())
        return list(session.scalars(query))


def select_accepted_response(order_id: int) -> Response | None:
    """Находит принятый отклик по заказу, если исполнитель уже выбран."""

    with get_session() as session:
        query = select(Response).where(Response.order_id == order_id, Response.status == ResponseStatus.ACCEPTED)
        return session.scalar(query)


def response_exists_for_order_and_executor(order_id: int, executor_id: int) -> bool:
    """Проверяет, откликался ли уже этот исполнитель на этот заказ."""

    with get_session() as session:
        query = select(Response.id).where(Response.order_id == order_id, Response.executor_id == executor_id)
        return session.scalar(query) is not None


def update_response_status(response_id: int, status: str):
    """Меняет статус отклика."""

    with get_session() as session:
        response = session.get(Response, response_id)
        if response is None:
            return None
        response.status = status
        session.commit()
        return response


def reject_other_responses(order_id: int, keep_response_id: int):
    """Отклоняет все отклики на заказ, кроме выбранного."""

    with get_session() as session:
        query = select(Response).where(Response.order_id == order_id, Response.id != keep_response_id)
        for response in session.scalars(query):
            response.status = ResponseStatus.REJECTED
        session.commit()


def count_response_media(response_id: int) -> int:
    """Считает количество медиафайлов, прикреплённых к отклику."""

    with get_session() as session:
        query = select(ResponseMedia.id).where(ResponseMedia.response_id == response_id)
        return len(list(session.scalars(query)))
