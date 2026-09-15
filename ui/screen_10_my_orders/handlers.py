"""Обработчики списка собственных заказов и откликов."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from services.order_service import get_categories, get_my_orders, get_order
from services.response_service import get_my_responses
from services.user_service import register_or_get_user
from ui.common import send_screen
from ui.screen_10_my_orders.keyboards import get_screen_10_my_orders_keyboard, get_to_main_menu_keyboard
from ui.screen_10_my_orders.texts import NO_MY_ORDERS_TEXT, get_screen_10_my_orders_text, get_status_label
from ui.states import OrderStates


@bot.message_handler(func=lambda message: message.text == "Мои заказы")
def message_open_my_orders_handler(message: types.Message, state: StateContext):
    """Собирает список заказов и откликов пользователя и показывает первую карточку."""

    telegram_user = message.from_user
    user = register_or_get_user(telegram_user.id, telegram_user.username, telegram_user.full_name)

    client_orders = get_my_orders(user.id)
    executor_responses = get_my_responses(user.id)
    items = [{"role": "client", "order_id": order.id} for order in client_orders]
    items += [{"role": "executor", "order_id": response.order_id} for response in executor_responses]

    if not items:
        state.set(OrderStates.screen_10_my_orders)
        send_screen(message.chat.id, state, NO_MY_ORDERS_TEXT, get_to_main_menu_keyboard())
        return

    state.set(OrderStates.screen_10_my_orders)
    state.add_data(my_orders_items=items, my_orders_index=0)
    show_screen_10_my_orders_card(message.chat.id, state)


def show_screen_10_my_orders_card(chat_id: int, state: StateContext):
    """Показывает карточку заказа или отклика по текущему индексу списка."""

    with state.data() as data:
        items = data["my_orders_items"]
        index = data["my_orders_index"]

    item = items[index]
    order = get_order(item["order_id"])
    categories_by_id = {category.id: category.name for category in get_categories()}
    role_text = "мой заказ" if item["role"] == "client" else "мой отклик"

    text = get_screen_10_my_orders_text(
        index + 1, len(items), role_text, categories_by_id.get(order.category_id, "—"),
        get_status_label(order.status), float(order.budget_rub),
    )
    keyboard = get_screen_10_my_orders_keyboard(has_prev=index > 0, has_next=index < len(items) - 1)
    send_screen(chat_id, state, text, keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("myorders:"), state=OrderStates.screen_10_my_orders)
def callback_screen_10_my_orders_handler(call: types.CallbackQuery, state: StateContext):
    """Листает список заказов и откликов или открывает выбранную карточку."""

    bot.answer_callback_query(call.id)
    action = call.data.split(":", 1)[1]

    with state.data() as data:
        index = data["my_orders_index"]

    if action == "next":
        state.add_data(my_orders_index=index + 1)
        show_screen_10_my_orders_card(call.message.chat.id, state)
        return

    if action == "prev" and index > 0:
        state.add_data(my_orders_index=index - 1)
        show_screen_10_my_orders_card(call.message.chat.id, state)
        return

    if action == "open":
        with state.data() as data:
            item = data["my_orders_items"][data["my_orders_index"]]

        from ui.screen_11_order_card.handlers import show_screen_11_order_card

        show_screen_11_order_card(call.message.chat.id, state, item["order_id"], item["role"])
