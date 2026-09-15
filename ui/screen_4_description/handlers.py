"""Обработчик ввода описания заказа."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from services.order_service import validate_description
from ui.screen_4_description.keyboards import get_back_only_keyboard
from ui.screen_4_description.texts import DESCRIPTION_INVALID_TEXT, get_screen_4_description_text
from ui.states import OrderStates


def show_screen_4_description(chat_id: int, state: StateContext):
    """Запрашивает у пользователя описание задачи."""

    state.set(OrderStates.screen_4_description)
    bot.send_message(chat_id, get_screen_4_description_text(), reply_markup=get_back_only_keyboard())


@bot.message_handler(state=OrderStates.screen_4_description)
def message_screen_4_description_handler(message: types.Message, state: StateContext):
    """Проверяет описание и переводит на экран бюджета либо просит ввести заново."""

    if message.text == "Назад":
        from ui.screen_3_category.handlers import show_screen_3_category

        show_screen_3_category(message.chat.id, state)
        return

    description = validate_description(message.text)
    if description is None:
        bot.send_message(message.chat.id, DESCRIPTION_INVALID_TEXT)
        return

    state.add_data(description=description)

    from ui.screen_5_budget.handlers import show_screen_5_currency

    show_screen_5_currency(message.chat.id, state)
