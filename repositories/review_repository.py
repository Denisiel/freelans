"""Операции чтения и записи взаимных оценок пользователей."""

from sqlalchemy import func, select

from models.order import Order
from models.response import Response, ResponseStatus
from models.review import Review
from repositories.database import get_session


def insert_review(order_id: int, from_user_id: int, to_user_id: int, rating: int,
                   comment: str | None = None) -> Review:
    """Сохраняет оценку, оставленную одной стороной заказа другой."""

    with get_session() as session:
        review = Review(
            order_id=order_id,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            rating=rating,
            comment=comment,
        )
        session.add(review)
        session.commit()
        return review


def review_exists(order_id: int, from_user_id: int) -> bool:
    """Проверяет, оставил ли пользователь уже обязательную оценку по заказу."""

    with get_session() as session:
        query = select(Review.id).where(Review.order_id == order_id, Review.from_user_id == from_user_id)
        return session.scalar(query) is not None


def select_average_rating_as_client(user_id: int) -> tuple[float | None, int]:
    """Средний рейтинг пользователя в роли заказчика и число оценок."""

    with get_session() as session:
        query = (
            select(func.avg(Review.rating), func.count(Review.id))
            .join(Order, Review.order_id == Order.id)
            .where(Review.to_user_id == user_id, Order.client_id == user_id)
        )
        avg_rating, count = session.execute(query).one()
        return (round(float(avg_rating), 1) if avg_rating else None, count or 0)


def select_average_rating_as_executor(user_id: int) -> tuple[float | None, int]:
    """Средний рейтинг пользователя в роли исполнителя и число оценок."""

    with get_session() as session:
        query = (
            select(func.avg(Review.rating), func.count(Review.id))
            .join(Order, Review.order_id == Order.id)
            .join(Response, (Response.order_id == Order.id) & (Response.status == ResponseStatus.ACCEPTED))
            .where(Review.to_user_id == user_id, Response.executor_id == user_id)
        )
        avg_rating, count = session.execute(query).one()
        return (round(float(avg_rating), 1) if avg_rating else None, count or 0)
