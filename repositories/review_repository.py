from sqlalchemy import func
from models.review import Review
from models.order import Order
from models.response import Response, ResponseStatus


class ReviewRepository:
    def __init__(self, session):
        self._session = session

    def create(self, order_id: int, from_user_id: int, to_user_id: int, rating: int, comment: str = None) -> Review:
        review = Review(
            order_id=order_id,
            from_user_id=from_user_id,
            to_user_id=to_user_id,
            rating=rating,
            comment=comment,
        )
        self._session.add(review)
        self._session.commit()
        return review

    def get_average_rating_as_client(self, user_id: int):
        result = (
            self._session.query(func.avg(Review.rating), func.count(Review.id))
            .join(Order, Review.order_id == Order.id)
            .filter(Review.to_user_id == user_id, Order.client_id == user_id)
            .one()
        )
        avg_rating, count = result
        return (round(float(avg_rating), 1) if avg_rating else None, count or 0)

    def get_average_rating_as_executor(self, user_id: int):
        result = (
            self._session.query(func.avg(Review.rating), func.count(Review.id))
            .join(Order, Review.order_id == Order.id)
            .join(Response, (Response.order_id == Order.id) & (Response.status == ResponseStatus.ACCEPTED))
            .filter(Review.to_user_id == user_id, Response.executor_id == user_id)
            .one()
        )
        avg_rating, count = result
        return (round(float(avg_rating), 1) if avg_rating else None, count or 0)

    def exists(self, order_id: int, from_user_id: int) -> bool:
        return (
            self._session.query(Review)
            .filter_by(order_id=order_id, from_user_id=from_user_id)
            .first()
            is not None
        )
