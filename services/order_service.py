from datetime import datetime
from repositories.order_repository import OrderRepository
from repositories.category_repository import CategoryRepository
from services.currency_service import CurrencyService, CurrencyConversionError
from models.order import OrderStatus


class OrderValidationError(Exception):
    pass


class OrderService:
    def __init__(self, order_repo: OrderRepository, category_repo: CategoryRepository,
                 currency_service: CurrencyService):
        self._order_repo = order_repo
        self._category_repo = category_repo
        self._currency_service = currency_service

    def get_categories(self):
        return self._category_repo.get_all()

    def validate_description(self, text: str) -> str:
        text = (text or "").strip()
        if not text or len(text) > 1000:
            raise OrderValidationError("Описание должно быть от 1 до 1000 символов.")
        return text

    def validate_budget(self, raw_value: str) -> float:
        try:
            value = float(raw_value.replace(",", "."))
        except (ValueError, AttributeError):
            raise OrderValidationError("Бюджет должен быть положительным числом. Попробуйте ещё раз.")
        if value <= 0:
            raise OrderValidationError("Бюджет должен быть положительным числом. Попробуйте ещё раз.")
        return value

    def validate_deadline(self, raw_value: str) -> datetime:
        try:
            deadline = datetime.strptime(raw_value.strip(), "%d.%m.%Y %H:%M")
        except (ValueError, AttributeError):
            raise OrderValidationError("Дата не может быть раньше сегодняшнего дня.")
        if deadline < datetime.now():
            raise OrderValidationError("Дата не может быть раньше сегодняшнего дня.")
        return deadline

    def calculate_budget_rub(self, budget: float, currency: str) -> float:
        try:
            return self._currency_service.convert_to_rub(budget, currency)
        except CurrencyConversionError as exc:
            raise OrderValidationError(str(exc)) from exc

    def publish_order(self, client_id: int, category_id: int, description: str,
                       budget: float, currency: str, budget_rub: float, deadline: datetime):
        return self._order_repo.create(
            client_id=client_id, category_id=category_id, description=description,
            budget=budget, currency=currency, budget_rub=budget_rub, deadline=deadline,
        )

    def get_feed(self, viewer_client_id: int):
        return self._order_repo.get_open_orders(exclude_client_id=viewer_client_id)

    def get_my_orders(self, client_id: int):
        return self._order_repo.get_orders_by_client(client_id)

    def get_order(self, order_id: int):
        return self._order_repo.get_by_id(order_id)

    def start_progress(self, order_id: int):
        return self._order_repo.update_status(order_id, OrderStatus.IN_PROGRESS)

    def mark_disputed(self, order_id: int):
        return self._order_repo.update_status(order_id, OrderStatus.DISPUTED)

    def mark_completed(self, order_id: int):
        return self._order_repo.update_status(order_id, OrderStatus.COMPLETED)
