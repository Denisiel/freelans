"""Обработчики просмотра ленты открытых заказов."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from services.order_service import get_categories, get_feed, get_order
from services.user_service import register_or_get_user
from ui.common import send_screen
from ui.screen_8_feed.keyboards import get_screen_8_feed_keyboard, get_to_main_menu_keyboard
from ui.screen_8_feed.texts import END_OF_LIST_TEXT, NO_OPEN_ORDERS_TEXT, get_screen_8_feed_text
from ui.states import OrderStates


@bot.message_handler(func=lambda message: message.text == "Лента заказов")
def message_open_feed_handler(message: types.Message, state: StateContext):
    """Открывает ленту открытых заказов, кроме заказов самого пользователя."""

    telegram_user = message.from_user
    user = register_or_get_user(telegram_user.id, telegram_user.username, telegram_user.full_name)
    orders = get_feed(user.id)

    if not orders:
        state.set(OrderStates.screen_8_feed)
        send_screen(message.chat.id, state, NO_OPEN_ORDERS_TEXT, get_to_main_menu_keyboard())
        return

    state.set(OrderStates.screen_8_feed)
    state.add_data(feed_order_ids=[order.id for order in orders], feed_index=0)
    show_screen_8_feed_card(message.chat.id, state)


def show_screen_8_feed_card(chat_id: int, state: StateContext):
    """Показывает карточку заказа по текущему индексу ленты."""

    with state.data() as data:
        order_ids = data["feed_order_ids"]
        index = data["feed_index"]

    if index >= len(order_ids):
        send_screen(chat_id, state, END_OF_LIST_TEXT, get_to_main_menu_keyboard())
        return

    order = get_order(order_ids[index])
    categories_by_id = {category.id: category.name for category in get_categories()}

    text = get_screen_8_feed_text(
        index + 1, len(order_ids), categories_by_id.get(order.category_id, "—"),
        order.description, float(order.budget_rub), order.deadline_hours,
    )
    keyboard = get_screen_8_feed_keyboard(has_prev=index > 0, has_next=index < len(order_ids) - 1)
    send_screen(chat_id, state, text, keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith("feed:"), state=OrderStates.screen_8_feed)
def callback_screen_8_feed_handler(call: types.CallbackQuery, state: StateContext):
    """Листает ленту заказов или переходит к отклику на текущий заказ."""

    bot.answer_callback_query(call.id)
    action = call.data.split(":", 1)[1]

    with state.data() as data:
        index = data["feed_index"]

    if action == "next":
        state.add_data(feed_index=index + 1)
        show_screen_8_feed_card(call.message.chat.id, state)
        return

    if action == "prev" and index > 0:
        state.add_data(feed_index=index - 1)
        show_screen_8_feed_card(call.message.chat.id, state)
        return

    if action == "respond":
        with state.data() as data:
            order_id = data["feed_order_ids"][data["feed_index"]]
        state.add_data(response_order_id=order_id, response_price=None, response_comment=None, response_media=[])

        from ui.screen_9_response.handlers import show_screen_9_response_menu

        show_screen_9_response_menu(call.message.chat.id, state)
