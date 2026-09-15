"""Бизнес-операции оценок пользователей после завершения заказа."""

from models.review import Review
from repositories.review_repository import (
    insert_review,
    review_exists,
    select_average_rating_as_client,
    select_average_rating_as_executor,
)


def has_rated(order_id: int, user_id: int) -> bool:
    """Проверяет, оставил ли пользователь уже обязательную оценку по заказу."""

    return review_exists(order_id, user_id)


def submit_review(order_id: int, from_user_id: int, to_user_id: int, rating: int,
                   comment: str | None = None) -> Review:
    """Сохраняет оценку одной стороны заказа другой стороне."""

    return insert_review(order_id, from_user_id, to_user_id, rating, comment)


def get_profile_stats(user_id: int) -> dict:
    """Возвращает средний рейтинг пользователя отдельно как заказчика и исполнителя."""

    return {
        "client": select_average_rating_as_client(user_id),
        "executor": select_average_rating_as_executor(user_id),
    }
