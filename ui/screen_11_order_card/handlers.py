"""Обработчики карточки заказа."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from models.order import Order
from services.order_service import get_categories, get_order
from services.rating_service import has_rated
from services.user_service import get_user_by_telegram_id
from ui.common import send_screen
from ui.screen_11_order_card.keyboards import get_screen_11_order_card_keyboard
from ui.screen_11_order_card.texts import UNDER_DEVELOPMENT_TEXT, get_screen_11_order_card_text
from ui.states import OrderStates


def get_action_buttons(role: str, order: Order, already_rated: bool) -> list[str]:
    """Определяет, какие кнопки действий доступны для роли и статуса заказа.

    Полный сценарий этих кнопок (экраны 12, 13, 15-17) — предмет следующего
    шага методички; сейчас они честно сообщают, что раздел в разработке.
    """

    buttons = []
    if role == "client" and order.status == "open":
        buttons.append("Посмотреть отклики")
    if role == "client" and order.status == "in_progress":
        buttons.append("Заказ выполнен?")
    if role == "executor" and order.status == "in_progress":
        buttons.append("Работа сдана")
    if order.status == "completed" and not already_rated:
        buttons.append("Оценить")
    return buttons


def show_screen_11_order_card(chat_id: int, state: StateContext, order_id: int, role: str):
    """Показывает подробную карточку заказа с кнопками, доступными для роли.

    В личном чате Telegram ID пользователя совпадает с ``chat_id``, поэтому
    отдельно передавать его не нужно.
    """

    order = get_order(order_id)
    categories_by_id = {category.id: category.name for category in get_categories()}
    user = get_user_by_telegram_id(chat_id)
    already_rated = has_rated(order_id, user.id) if user else False

    state.set(OrderStates.screen_11_order_card)
    state.add_data(order_card_id=order_id, order_card_role=role)

    text = get_screen_11_order_card_text(
        categories_by_id.get(order.category_id, "—"), order.description, float(order.budget_rub),
        order.deadline, order.deadline_hours, order.status,
    )
    buttons = get_action_buttons(role, order, already_rated)
    send_screen(chat_id, state, text, get_screen_11_order_card_keyboard(buttons))


@bot.callback_query_handler(func=lambda call: call.data.startswith("card:"), state=OrderStates.screen_11_order_card)
def callback_screen_11_order_card_handler(call: types.CallbackQuery, state: StateContext):
    """Обрабатывает нажатия кнопок карточки заказа."""

    bot.answer_callback_query(call.id)
    action = call.data.split(":", 1)[1]

    if action == "back":
        state.set(OrderStates.screen_10_my_orders)

        from ui.screen_10_my_orders.handlers import show_screen_10_my_orders_card

        show_screen_10_my_orders_card(call.message.chat.id, state)
        return

    if action in ("responses", "complete", "deliver", "rate"):
        bot.send_message(call.message.chat.id, UNDER_DEVELOPMENT_TEXT)
