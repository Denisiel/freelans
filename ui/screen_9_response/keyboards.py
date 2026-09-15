"""Клавиатуры экрана отклика на заказ и его подэкранов."""

import telebot


def get_screen_9_response_menu_keyboard() -> telebot.types.InlineKeyboardMarkup:
    """Строит клавиатуру-конструктор отклика: цена, комментарий, медиа, отправка."""

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("Указать цену", callback_data="response:price"))
    keyboard.add(telebot.types.InlineKeyboardButton("Указать комментарий", callback_data="response:comment"))
    keyboard.add(telebot.types.InlineKeyboardButton("Прикрепить медиафайлы", callback_data="response:media"))
    keyboard.add(telebot.types.InlineKeyboardButton("Отправить отклик", callback_data="response:send"))
    keyboard.add(telebot.types.InlineKeyboardButton("Назад", callback_data="response:back"))
    return keyboard


def get_back_only_keyboard() -> telebot.types.ReplyKeyboardMarkup:
    """Создаёт клавиатуру с единственной кнопкой «Назад» рядом с полем ввода."""

    keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(telebot.types.KeyboardButton("Назад"))
    return keyboard


def get_screen_9_media_keyboard() -> telebot.types.InlineKeyboardMarkup:
    """Строит клавиатуру подэкрана прикрепления медиафайлов."""

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("Готово", callback_data="media:done"))
    keyboard.add(telebot.types.InlineKeyboardButton("Назад", callback_data="media:back"))
    return keyboard
