"""Клавиатура экрана профиля."""

import telebot


def get_to_main_menu_keyboard() -> telebot.types.InlineKeyboardMarkup:
    """Создаёт клавиатуру с единственной кнопкой возврата в главное меню."""

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("В главное меню", callback_data="menu:main"))
    return keyboard
