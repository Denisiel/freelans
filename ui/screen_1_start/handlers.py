"""Обработчик команды ``/start``."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from services.user_service import get_user_by_telegram_id, register_or_get_user
from ui.screen_1_start.keyboards import get_screen_1_start_keyboard
from ui.screen_1_start.texts import get_screen_1_start_text

# Импорт screen_2_main_menu.handlers сделан внутри функций, а не здесь.
# На верхнем уровне модуля он заставил бы screen_2 зарегистрировать свои
# обработчики (включая «ловушку» нераспознанного текста) раньше screen_1,
# и порядок импортов в main.py перестал бы что-либо решать.


@bot.message_handler(commands=["start"])
def command_screen_1_start_handler(message: types.Message, state: StateContext):
    """Показывает приветствие новому пользователю или сразу открывает меню.

    ``/start`` должен возвращать пользователя в главное меню независимо от
    того, на каком экране он находится. Экран приветствия при этом нужен
    только один раз — при самом первом обращении к боту.
    """

    from ui.screen_2_main_menu.handlers import show_screen_2_main_menu

    if get_user_by_telegram_id(message.from_user.id) is not None:
        show_screen_2_main_menu(message.chat.id, state)
        return

    state.delete()
    bot.send_message(
        message.chat.id,
        get_screen_1_start_text(),
        reply_markup=get_screen_1_start_keyboard(),
    )


@bot.message_handler(func=lambda message: message.text == "Старт")
def message_screen_1_start_button_handler(message: types.Message, state: StateContext):
    """Регистрирует нового пользователя и переводит его в главное меню."""

    from ui.screen_2_main_menu.handlers import show_screen_2_main_menu

    telegram_user = message.from_user
    register_or_get_user(telegram_user.id, telegram_user.username, telegram_user.full_name)
    show_screen_2_main_menu(message.chat.id, state)
