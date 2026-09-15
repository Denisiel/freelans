"""Обработчики выбора категории заказа."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from services.order_service import get_categories, get_category
from ui.common import send_screen
from ui.screen_2_main_menu.texts import UNKNOWN_COMMAND_TEXT
from ui.screen_3_category.keyboards import get_screen_3_category_keyboard
from ui.screen_3_category.texts import get_screen_3_category_text
from ui.states import OrderStates


def show_screen_3_category(chat_id: int, state: StateContext):
    """Показывает список категорий для нового заказа."""

    state.set(OrderStates.screen_3_category)
    categories = get_categories()
    send_screen(chat_id, state, get_screen_3_category_text(), get_screen_3_category_keyboard(categories))


@bot.message_handler(func=lambda message: message.text == "Создать заказ")
def message_create_order_handler(message: types.Message, state: StateContext):
    """Запускает сценарий создания заказа с выбора категории."""

    show_screen_3_category(message.chat.id, state)


@bot.callback_query_handler(func=lambda call: call.data.startswith("category:"), state=OrderStates.screen_3_category)
def callback_screen_3_category_handler(call: types.CallbackQuery, state: StateContext):
    """Сохраняет выбранную категорию и переводит на экран описания."""

    bot.answer_callback_query(call.id)
    action = call.data.split(":", 1)[1]

    if action == "back":
        # Локальный импорт не даёт возникнуть циклу: главное меню, в свою
        # очередь, ведёт на этот же экран через кнопку «Создать заказ».
        from ui.screen_2_main_menu.handlers import show_screen_2_main_menu

        show_screen_2_main_menu(call.message.chat.id, state)
        return

    category = get_category(int(action))
    if category is None:
        bot.send_message(call.message.chat.id, UNKNOWN_COMMAND_TEXT)
        return

    state.add_data(category_id=category.id, category_name=category.name)

    from ui.screen_4_description.handlers import show_screen_4_description

    show_screen_4_description(call.message.chat.id, state)
