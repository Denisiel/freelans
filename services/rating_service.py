from repositories.review_repository import ReviewRepository


class RatingValidationError(Exception):
    pass


class RatingService:
    def __init__(self, review_repo: ReviewRepository):
        self._review_repo = review_repo

    def submit_review(self, order_id: int, from_user_id: int, to_user_id: int,
                       rating: int, comment: str = None):
        if rating not in (1, 2, 3, 4, 5):
            raise RatingValidationError("Оценка должна быть от 1 до 5.")
        if self._review_repo.exists(order_id, from_user_id):
            raise RatingValidationError("Вы уже оценили этот заказ.")
        return self._review_repo.create(order_id, from_user_id, to_user_id, rating, comment)

    def get_profile_stats(self, user_id: int):
        return {
            "client": self._review_repo.get_average_rating_as_client(user_id),
            "executor": self._review_repo.get_average_rating_as_executor(user_id),
        }
