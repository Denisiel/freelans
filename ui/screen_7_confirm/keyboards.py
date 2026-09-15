"""Клавиатура экрана подтверждения заказа."""

import telebot


def get_screen_7_confirm_keyboard() -> telebot.types.InlineKeyboardMarkup:
    """Создаёт клавиатуру с кнопками публикации и возврата к предыдущему шагу."""

    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(telebot.types.InlineKeyboardButton("Опубликовать", callback_data="confirm:publish"))
    keyboard.add(telebot.types.InlineKeyboardButton("Назад", callback_data="confirm:back"))
    return keyboard
