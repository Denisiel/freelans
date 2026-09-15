"""Обработчики главного меню и функция его показа."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from ui.common import send_screen
from ui.screen_2_main_menu.keyboards import get_screen_2_main_menu_keyboard
from ui.screen_2_main_menu.texts import UNKNOWN_COMMAND_TEXT, get_screen_2_main_menu_text
from ui.states import OrderStates


def show_screen_2_main_menu(chat_id: int, state: StateContext):
    """Переключает диалог на главное меню и отправляет его содержимое.

    Функция вынесена отдельно, потому что главное меню нужно показывать не
    только после ``/start``, но и после возврата практически с любого экрана.
    """

    # Прошлый сценарий и его временные данные больше не нужны.
    state.delete()
    state.set(OrderStates.screen_2_main_menu)
    send_screen(chat_id, state, get_screen_2_main_menu_text(), get_screen_2_main_menu_keyboard())


@bot.message_handler(func=lambda message: message.text == "В главное меню")
def handle_back_to_main_menu(message: types.Message, state: StateContext):
    """Кнопка «В главное меню» работает одинаково из любого состояния диалога."""

    show_screen_2_main_menu(message.chat.id, state)


@bot.callback_query_handler(func=lambda call: call.data == "menu:main")
def handle_back_to_main_menu_callback(call: types.CallbackQuery, state: StateContext):
    """Inline-вариант кнопки «В главное меню» на экранах с inline-клавиатурой."""

    bot.answer_callback_query(call.id)
    show_screen_2_main_menu(call.message.chat.id, state)


# Этот обработчик должен быть зарегистрирован последним (см. порядок импортов
# в main.py): он реагирует на любой текст, не распознанный обработчиками
# конкретных экранов, и не должен перехватывать их сообщения.
@bot.message_handler(func=lambda message: True)
def handle_unknown_command(message: types.Message, state: StateContext):
    """Сообщает о нераспознанной команде, не меняя текущий экран пользователя."""

    bot.send_message(message.chat.id, UNKNOWN_COMMAND_TEXT)
