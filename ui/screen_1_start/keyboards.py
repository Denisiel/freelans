"""Клавиатура приветственного экрана."""

import telebot


def get_screen_1_start_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """Создаёт клавиатуру с единственной кнопкой запуска бота."""

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton("Старт"))
    return keyboard
