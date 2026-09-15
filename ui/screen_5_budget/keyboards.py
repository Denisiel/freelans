"""Клавиатуры экрана указания бюджета и валюты заказа."""

import telebot


def get_screen_5_currency_keyboard() -> telebot.types.InlineKeyboardMarkup:
    """Строит клавиатуру выбора валюты бюджета."""

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton("RUB", callback_data="currency:RUB"),
        telebot.types.InlineKeyboardButton("USD", callback_data="currency:USD"),
        telebot.types.InlineKeyboardButton("EUR", callback_data="currency:EUR"),
    )
    keyboard.add(telebot.types.InlineKeyboardButton("Назад", callback_data="currency:back"))
    return keyboard


def get_back_only_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """Создаёт клавиатуру с единственной кнопкой «Назад» рядом с полем ввода."""

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton("Назад"))
    return keyboard
