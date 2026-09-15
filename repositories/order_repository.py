"""Операции чтения и записи заказов."""

import datetime

from sqlalchemy import select

from models.order import Order, OrderStatus
from repositories.database import get_session


def insert_order(client_id: int, category_id: int, description: str, budget: float,
                  currency: str, budget_rub: float, deadline_hours: int) -> Order:
    """Сохраняет новый заказ со статусом ``open``."""

    with get_session() as session:
        order = Order(
            client_id=client_id,
            category_id=category_id,
            description=description,
            budget=budget,
            currency=currency,
            budget_rub=budget_rub,
            deadline_hours=deadline_hours,
            status=OrderStatus.OPEN,
        )
        session.add(order)
        session.commit()
        session.refresh(order)
        return order


def select_order_by_id(order_id: int) -> Order | None:
    """Находит заказ по идентификатору."""

    with get_session() as session:
        return session.get(Order, order_id)


def select_open_orders(exclude_client_id: int) -> list[Order]:
    """Возвращает открытые заказы, кроме заказов самого пользователя."""

    with get_session() as session:
        query = (
            select(Order)
            .where(Order.status == OrderStatus.OPEN, Order.client_id != exclude_client_id)
            .order_by(Order.created_at.desc())
        )
        return list(session.scalars(query))


def select_orders_by_client(client_id: int) -> list[Order]:
    """Возвращает заказы, где пользователь выступает заказчиком."""

    with get_session() as session:
        query = select(Order).where(Order.client_id == client_id).order_by(Order.created_at.desc())
        return list(session.scalars(query))


def update_order_status(order_id: int, status: str):
    """Меняет статус заказа."""

    with get_session() as session:
        order = session.get(Order, order_id)
        if order is None:
            return None
        order.status = status
        session.commit()
        return order


def update_order_deadline(order_id: int, deadline: datetime.datetime):
    """Проставляет точную дату дедлайна после выбора исполнителя."""

    with get_session() as session:
        order = session.get(Order, order_id)
        if order is None:
            return None
        order.deadline = deadline
        session.commit()
        return order
