"""Общая вспомогательная функция, используемая обработчиками всех экранов."""

import telebot

from bot_instance import bot


def send_screen(chat_id: int, state, text: str, keyboard=None) -> telebot.types.Message:
    """Отправляет содержимое экрана и убирает inline-кнопки с предыдущего.

    Telegram не ограничивает, сколько сообщений с inline-кнопками может
    оставаться в чате одновременно, поэтому без этой функции нажатие кнопки
    на уже покинутом экране могло бы запускать устаревший обработчик.
    """

    with state.data() as data:
        previous_message_id = data.get("last_inline_message_id")

    if previous_message_id:
        try:
            bot.edit_message_reply_markup(chat_id, previous_message_id, reply_markup=None)
        except Exception:
            # Сообщение могло быть удалено или устареть — это не мешает боту работать дальше.
            pass

    message = bot.send_message(chat_id, text, reply_markup=keyboard)

    # Запоминаем id только для inline-клавиатур: у обычной клавиатуры нет
    # отдельных кнопок на конкретном сообщении, чистить нечего.
    if isinstance(keyboard, telebot.types.InlineKeyboardMarkup):
        state.add_data(last_inline_message_id=message.message_id)

    return message
