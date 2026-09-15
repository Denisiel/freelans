"""Клавиатура экрана ввода описания заказа."""

import telebot


def get_back_only_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """Создаёт клавиатуру с единственной кнопкой «Назад» рядом с полем ввода."""

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton("Назад"))
    return keyboard
