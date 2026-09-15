"""Обработчики конструктора отклика на заказ и его подэкранов."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from services.order_service import get_order
from services.response_service import (
    has_already_responded,
    is_own_order,
    submit_response,
    validate_comment,
    validate_price,
)
from services.user_service import register_or_get_user
from ui.common import send_screen
from ui.screen_9_response.keyboards import (
    get_back_only_keyboard,
    get_screen_9_media_keyboard,
    get_screen_9_response_menu_keyboard,
)
from ui.screen_9_response.texts import (
    ALREADY_RESPONDED_TEXT,
    ASK_COMMENT_TEXT,
    ASK_MEDIA_TEXT,
    ASK_PRICE_TEXT,
    CANNOT_RESPOND_OWN_ORDER_TEXT,
    COMMENT_TOO_LONG_TEXT,
    NEED_PRICE_FIRST_TEXT,
    PRICE_INVALID_TEXT,
    RESPONSE_SENT_TEXT,
    get_screen_9_response_menu_text,
)
from ui.states import OrderStates


def show_screen_9_response_menu(chat_id: int, state: StateContext):
    """Показывает текущий черновик отклика и кнопки его заполнения."""

    state.set(OrderStates.screen_9_menu)

    with state.data() as data:
        price_text = f"{data['response_price']:g}" if data.get("response_price") else "не указана"
        comment_text = data.get("response_comment") or "не указан"
        media_count = len(data.get("response_media") or [])

    text = get_screen_9_response_menu_text(price_text, comment_text, media_count)
    send_screen(chat_id, state, text, get_screen_9_response_menu_keyboard())


@bot.callback_query_handler(func=lambda call: call.data.startswith("response:"), state=OrderStates.screen_9_menu)
def callback_screen_9_response_menu_handler(call: types.CallbackQuery, state: StateContext):
    """Направляет нажатие кнопки конструктора отклика на нужный подэкран."""

    bot.answer_callback_query(call.id)
    chat_id = call.message.chat.id
    action = call.data.split(":", 1)[1]

    if action == "back":
        state.set(OrderStates.screen_8_feed)

        from ui.screen_8_feed.handlers import show_screen_8_feed_card

        show_screen_8_feed_card(chat_id, state)
        return

    if action == "price":
        state.set(OrderStates.screen_9_price)
        bot.send_message(chat_id, ASK_PRICE_TEXT, reply_markup=get_back_only_keyboard())
        return

    if action == "comment":
        state.set(OrderStates.screen_9_comment)
        bot.send_message(chat_id, ASK_COMMENT_TEXT, reply_markup=get_back_only_keyboard())
        return

    if action == "media":
        state.set(OrderStates.screen_9_media)
        send_screen(chat_id, state, ASK_MEDIA_TEXT, get_screen_9_media_keyboard())
        return

    if action == "send":
        with state.data() as data:
            price = data.get("response_price")
            order_id = data["response_order_id"]
            comment = data.get("response_comment")
            media_file_ids = data.get("response_media") or []

        if not price:
            bot.send_message(chat_id, NEED_PRICE_FIRST_TEXT)
            return

        order = get_order(order_id)
        telegram_user = call.from_user
        user = register_or_get_user(telegram_user.id, telegram_user.username, telegram_user.full_name)

        if is_own_order(order, user.id):
            bot.send_message(chat_id, CANNOT_RESPOND_OWN_ORDER_TEXT)
            return
        if has_already_responded(order_id, user.id):
            bot.send_message(chat_id, ALREADY_RESPONDED_TEXT)
            return

        submit_response(order_id, user.id, price, comment, media_file_ids)
        bot.send_message(chat_id, RESPONSE_SENT_TEXT)

        from ui.screen_2_main_menu.handlers import show_screen_2_main_menu

        show_screen_2_main_menu(chat_id, state)


@bot.message_handler(state=OrderStates.screen_9_price)
def message_screen_9_price_handler(message: types.Message, state: StateContext):
    """Проверяет цену отклика и возвращает в конструктор отклика."""

    if message.text == "Назад":
        show_screen_9_response_menu(message.chat.id, state)
        return

    price = validate_price(message.text)
    if price is None:
        bot.send_message(message.chat.id, PRICE_INVALID_TEXT)
        return

    state.add_data(response_price=price)
    show_screen_9_response_menu(message.chat.id, state)


@bot.message_handler(state=OrderStates.screen_9_comment)
def message_screen_9_comment_handler(message: types.Message, state: StateContext):
    """Проверяет комментарий отклика и возвращает в конструктор отклика."""

    if message.text == "Назад":
        show_screen_9_response_menu(message.chat.id, state)
        return

    comment = validate_comment(message.text)
    if comment is None:
        bot.send_message(message.chat.id, COMMENT_TOO_LONG_TEXT)
        return

    state.add_data(response_comment=comment)
    show_screen_9_response_menu(message.chat.id, state)


@bot.message_handler(state=OrderStates.screen_9_media, content_types=["photo", "document"])
def message_screen_9_media_file_handler(message: types.Message, state: StateContext):
    """Добавляет присланный файл в список медиа текущего отклика."""

    file_id = message.photo[-1].file_id if message.photo else message.document.file_id

    with state.data() as data:
        media = data.get("response_media") or []
    media.append(file_id)
    state.add_data(response_media=media)

    send_screen(
        message.chat.id, state,
        f"{ASK_MEDIA_TEXT}\nПрикреплено: {len(media)} файл(ов)",
        get_screen_9_media_keyboard(),
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("media:"), state=OrderStates.screen_9_media)
def callback_screen_9_media_handler(call: types.CallbackQuery, state: StateContext):
    """И «Готово», и «Назад» одинаково возвращают в конструктор отклика."""

    bot.answer_callback_query(call.id)
    show_screen_9_response_menu(call.message.chat.id, state)
