from models.user import User


class UserRepository:
    def __init__(self, session):
        self._session = session

    def get_by_telegram_id(self, telegram_id: int):
        return self._session.query(User).filter_by(telegram_id=telegram_id).first()

    def create(self, telegram_id: int, username: str, full_name: str) -> User:
        user = User(telegram_id=telegram_id, username=username, full_name=full_name)
        self._session.add(user)
        self._session.commit()
        return user

    def get_or_create(self, telegram_id: int, username: str, full_name: str) -> User:
        user = self.get_by_telegram_id(telegram_id)
        if user is not None:
            return user
        return self.create(telegram_id, username, full_name)
