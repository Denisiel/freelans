"""Клавиатура экрана карточки заказа."""

import telebot

# Каждой кнопке действия соответствует своё служебное значение callback_data.
# Набор доступных кнопок зависит от роли пользователя и статуса заказа —
# это вычисляет services/order_service.py и передаёт сюда список подписей.
ACTION_CALLBACKS = {
    "Посмотреть отклики": "card:responses",
    "Заказ выполнен?": "card:complete",
    "Работа сдана": "card:deliver",
    "Оценить": "card:rate",
}


def get_screen_11_order_card_keyboard(action_buttons: list[str]) -> telebot.types.InlineKeyboardMarkup:
    """Строит клавиатуру карточки с кнопками, доступными для роли и статуса."""

    keyboard = telebot.types.InlineKeyboardMarkup()
    for label in action_buttons:
        keyboard.add(telebot.types.InlineKeyboardButton(label, callback_data=ACTION_CALLBACKS[label]))
    keyboard.row(
        telebot.types.InlineKeyboardButton("Назад", callback_data="card:back"),
        telebot.types.InlineKeyboardButton("В главное меню", callback_data="menu:main"),
    )
    return keyboard
