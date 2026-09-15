"""Создание общего экземпляра Telegram-бота.

Модуль отделён от ``main.py``, чтобы обработчики из разных экранов могли
импортировать один и тот же объект ``bot`` и регистрироваться в нём.
"""

import telebot
from telebot.storage import StateMemoryStorage

import config

# Создаём единственный экземпляр TeleBot для всего приложения.
bot = telebot.TeleBot(
    config.BOT_TOKEN,
    # Состояния диалога хранятся в оперативной памяти. После перезапуска
    # программы они сбросятся, что допустимо для учебного проекта.
    state_storage=StateMemoryStorage(),
    # Разрешаем middleware-классы, в том числе StateMiddleware из main.py.
    use_class_middlewares=True,
)
