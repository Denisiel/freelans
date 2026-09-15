"""Клавиатуры экрана списка собственных заказов и откликов."""

import telebot


def get_screen_10_my_orders_keyboard(has_prev: bool, has_next: bool) -> telebot.types.InlineKeyboardMarkup:
    """Строит клавиатуру карточки списка с учётом доступной навигации."""

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("Открыть карточку", callback_data="myorders:open"))

    navigation_row = []
    if has_prev:
        navigation_row.append(telebot.types.InlineKeyboardButton("Назад", callback_data="myorders:prev"))
    if has_next:
        navigation_row.append(telebot.types.InlineKeyboardButton("Дальше", callback_data="myorders:next"))
    if navigation_row:
        keyboard.row(*navigation_row)

    keyboard.add(telebot.types.InlineKeyboardButton("В главное меню", callback_data="menu:main"))
    return keyboard


def get_to_main_menu_keyboard() -> telebot.types.InlineKeyboardMarkup:
    """Создаёт клавиатуру с единственной кнопкой возврата в главное меню."""

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("В главное меню", callback_data="menu:main"))
    return keyboard
