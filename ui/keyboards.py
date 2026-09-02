from telebot import types


def start_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Старт"))
    return kb


def main_menu_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Создать заказ"))
    kb.add(types.KeyboardButton("Лента заказов"))
    kb.add(types.KeyboardButton("Мои заказы"))
    kb.add(types.KeyboardButton("Профиль"))
    return kb


def categories_kb(categories):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for cat in categories:
        kb.add(types.KeyboardButton(cat.name))
    kb.add(types.KeyboardButton("Назад"))
    return kb


def back_only_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Назад"))
    return kb


def currency_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("RUB"), types.KeyboardButton("USD"), types.KeyboardButton("EUR"))
    kb.add(types.KeyboardButton("Назад"))
    return kb


def order_preview_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Опубликовать"))
    kb.add(types.KeyboardButton("Назад"))
    return kb


def feed_kb(has_prev: bool, has_next: bool):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Откликнуться"))
    row = []
    if has_prev:
        row.append(types.KeyboardButton("Назад"))
    if has_next:
        row.append(types.KeyboardButton("Дальше"))
    if row:
        kb.add(*row)
    kb.add(types.KeyboardButton("В главное меню"))
    return kb


def to_main_menu_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("В главное меню"))
    return kb


def response_menu_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Указать цену"))
    kb.add(types.KeyboardButton("Указать комментарий"))
    kb.add(types.KeyboardButton("Прикрепить медиафайлы"))
    kb.add(types.KeyboardButton("Отправить отклик"))
    kb.add(types.KeyboardButton("Назад"))
    return kb


def media_kb():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(types.KeyboardButton("Готово"))
    kb.add(types.KeyboardButton("Назад"))
    return kb
