from datetime import datetime
from models.order import Order, OrderStatus


class OrderRepository:
    def __init__(self, session):
        self._session = session

    def create(self, client_id: int, category_id: int, description: str,
               budget: float, currency: str, budget_rub: float, deadline: datetime) -> Order:
        order = Order(
            client_id=client_id,
            category_id=category_id,
            description=description,
            budget=budget,
            currency=currency,
            budget_rub=budget_rub,
            deadline=deadline,
            status=OrderStatus.OPEN,
        )
        self._session.add(order)
        self._session.commit()
        return order

    def get_by_id(self, order_id: int):
        return self._session.query(Order).filter_by(id=order_id).first()

    def get_open_orders(self, exclude_client_id: int):
        return (
            self._session.query(Order)
            .filter(Order.status == OrderStatus.OPEN, Order.client_id != exclude_client_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    def get_orders_by_client(self, client_id: int):
        return (
            self._session.query(Order)
            .filter_by(client_id=client_id)
            .order_by(Order.created_at.desc())
            .all()
        )

    def update_status(self, order_id: int, status: str):
        order = self.get_by_id(order_id)
        if order is None:
            return None
        order.status = status
        self._session.commit()
        return order
