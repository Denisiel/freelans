"""Обработчики подтверждения и публикации заказа."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from services.order_service import publish_order
from services.user_service import register_or_get_user
from ui.common import send_screen
from ui.screen_7_confirm.keyboards import get_screen_7_confirm_keyboard
from ui.screen_7_confirm.texts import ORDER_PUBLISHED_TEXT, get_screen_7_confirm_text
from ui.states import OrderStates


def show_screen_7_confirm(chat_id: int, state: StateContext):
    """Показывает итоговую карточку заказа перед публикацией."""

    state.set(OrderStates.screen_7_confirm)

    with state.data() as data:
        text = get_screen_7_confirm_text(
            data["category_name"], data["description"], data["budget"], data["currency"], data["deadline_hours"]
        )

    send_screen(chat_id, state, text, get_screen_7_confirm_keyboard())


@bot.callback_query_handler(func=lambda call: call.data.startswith("confirm:"), state=OrderStates.screen_7_confirm)
def callback_screen_7_confirm_handler(call: types.CallbackQuery, state: StateContext):
    """Публикует заказ в базе данных либо возвращает к вводу срока."""

    bot.answer_callback_query(call.id)
    action = call.data.split(":", 1)[1]

    if action == "back":
        from ui.screen_6_deadline.handlers import show_screen_6_deadline

        show_screen_6_deadline(call.message.chat.id, state)
        return

    telegram_user = call.from_user
    user = register_or_get_user(telegram_user.id, telegram_user.username, telegram_user.full_name)

    with state.data() as data:
        publish_order(
            client_id=user.id,
            category_id=data["category_id"],
            description=data["description"],
            budget=data["budget"],
            currency=data["currency"],
            budget_rub=data["budget_rub"],
            deadline_hours=data["deadline_hours"],
        )

    bot.send_message(call.message.chat.id, ORDER_PUBLISHED_TEXT)

    from ui.screen_2_main_menu.handlers import show_screen_2_main_menu

    show_screen_2_main_menu(call.message.chat.id, state)
