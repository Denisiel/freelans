"""Обработчик ввода срока выполнения заказа."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from services.order_service import validate_deadline_hours
from ui.screen_6_deadline.keyboards import get_back_only_keyboard
from ui.screen_6_deadline.texts import DEADLINE_INVALID_TEXT, get_screen_6_deadline_text
from ui.states import OrderStates


def show_screen_6_deadline(chat_id: int, state: StateContext):
    """Запрашивает у пользователя срок выполнения в часах."""

    state.set(OrderStates.screen_6_deadline)
    bot.send_message(chat_id, get_screen_6_deadline_text(), reply_markup=get_back_only_keyboard())


@bot.message_handler(state=OrderStates.screen_6_deadline)
def message_screen_6_deadline_handler(message: types.Message, state: StateContext):
    """Проверяет срок и переходит к подтверждению заказа."""

    if message.text == "Назад":
        from ui.screen_5_budget.handlers import show_screen_5_budget_amount

        show_screen_5_budget_amount(message.chat.id, state)
        return

    deadline_hours = validate_deadline_hours(message.text)
    if deadline_hours is None:
        bot.send_message(message.chat.id, DEADLINE_INVALID_TEXT)
        return

    state.add_data(deadline_hours=deadline_hours)

    from ui.screen_7_confirm.handlers import show_screen_7_confirm

    show_screen_7_confirm(message.chat.id, state)
