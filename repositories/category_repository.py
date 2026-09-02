from models.category import Category


class CategoryRepository:
    def __init__(self, session):
        self._session = session

    def get_all(self):
        return self._session.query(Category).all()

    def get_by_id(self, category_id: int):
        return self._session.query(Category).filter_by(id=category_id).first()

    def seed_default_categories(self):
        if self._session.query(Category).count() > 0:
            return
        default_names = ["Дизайн", "Разработка", "Копирайтинг", "Маркетинг", "Другое"]
        for name in default_names:
            self._session.add(Category(name=name))
        self._session.commit()
