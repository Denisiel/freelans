"""Клавиатура экрана выбора категории заказа."""

import telebot

from models.category import Category


def get_screen_3_category_keyboard(categories: list[Category]) -> telebot.types.InlineKeyboardMarkup:
    """Строит по одной кнопке на каждую категорию справочника и кнопку «Назад»."""

    keyboard = telebot.types.InlineKeyboardMarkup()
    for category in categories:
        keyboard.add(
            telebot.types.InlineKeyboardButton(category.name, callback_data=f"category:{category.id}")
        )
    keyboard.add(telebot.types.InlineKeyboardButton("Назад", callback_data="category:back"))
    return keyboard
