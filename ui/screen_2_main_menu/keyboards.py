"""Клавиатура главного меню."""

import telebot


def get_screen_2_main_menu_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """Создаёт клавиатуру с четырьмя основными разделами приложения."""

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton("Создать заказ"))
    keyboard.add(telebot.types.KeyboardButton("Лента заказов"))
    keyboard.add(telebot.types.KeyboardButton("Мои заказы"))
    keyboard.add(telebot.types.KeyboardButton("Профиль"))
    return keyboard
