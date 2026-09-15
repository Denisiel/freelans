"""Клавиатуры экрана ленты открытых заказов."""

import telebot


def get_screen_8_feed_keyboard(has_prev: bool, has_next: bool) -> telebot.types.InlineKeyboardMarkup:
    """Строит клавиатуру карточки заказа с учётом доступной навигации."""

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("Откликнуться", callback_data="feed:respond"))

    navigation_row = []
    if has_prev:
        navigation_row.append(telebot.types.InlineKeyboardButton("Назад", callback_data="feed:prev"))
    if has_next:
        navigation_row.append(telebot.types.InlineKeyboardButton("Дальше", callback_data="feed:next"))
    if navigation_row:
        keyboard.row(*navigation_row)

    keyboard.add(telebot.types.InlineKeyboardButton("В главное меню", callback_data="menu:main"))
    return keyboard


def get_to_main_menu_keyboard() -> telebot.types.InlineKeyboardMarkup:
    """Создаёт клавиатуру с единственной кнопкой возврата в главное меню."""

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("В главное меню", callback_data="menu:main"))
    return keyboard
