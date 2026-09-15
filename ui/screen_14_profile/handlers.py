"""Обработчик экрана профиля пользователя."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from services.rating_service import get_profile_stats
from services.user_service import register_or_get_user
from ui.common import send_screen
from ui.screen_14_profile.keyboards import get_to_main_menu_keyboard
from ui.screen_14_profile.texts import get_screen_14_profile_text


@bot.message_handler(func=lambda message: message.text == "Профиль")
def message_open_profile_handler(message: types.Message, state: StateContext):
    """Показывает профиль пользователя с рейтингом заказчика и исполнителя."""

    telegram_user = message.from_user
    user = register_or_get_user(telegram_user.id, telegram_user.username, telegram_user.full_name)
    stats = get_profile_stats(user.id)

    client_avg, client_count = stats["client"]
    executor_avg, executor_count = stats["executor"]
    text = get_screen_14_profile_text(user.full_name, client_avg, client_count, executor_avg, executor_count)

    send_screen(message.chat.id, state, text, get_to_main_menu_keyboard())
