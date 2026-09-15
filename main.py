"""Точка входа в приложение FreelanceHub."""

from telebot import custom_filters
from telebot.states.sync.middleware import StateMiddleware

from bot_instance import bot
from repositories.category_repository import insert_default_categories
from repositories.database import create_all_tables

# Эти импорты нужны не для прямого вызова функций. При загрузке модулей
# декораторы @bot.message_handler и @bot.callback_query_handler регистрируют
# функции-обработчики в общем объекте bot. Модуль screen_2_main_menu импортирован
# последним: в нём объявлен обработчик-«ловушка» нераспознанного текста, который
# не должен перехватывать сообщения, предназначенные другим экранам.
import ui.screen_1_start.handlers
import ui.screen_3_category.handlers
import ui.screen_4_description.handlers
import ui.screen_5_budget.handlers
import ui.screen_6_deadline.handlers
import ui.screen_7_confirm.handlers
import ui.screen_8_feed.handlers
import ui.screen_9_response.handlers
import ui.screen_10_my_orders.handlers
import ui.screen_11_order_card.handlers
import ui.screen_14_profile.handlers
import ui.screen_2_main_menu.handlers

# После импортов настраиваем поддержку конечного автомата состояний.
# StateFilter позволяет ограничивать обработчики текущим состоянием диалога.
bot.add_custom_filter(custom_filters.StateFilter(bot))
# Middleware создаёт и передаёт аргумент StateContext в функции-обработчики.
bot.setup_middleware(StateMiddleware(bot))


def main():
    try:
        create_all_tables()
    except Exception as exc:
        print(f"Не удалось подключиться к базе данных: {exc}", flush=True)
        raise SystemExit(1)

    # Справочник категорий должен быть заполнен до первого запроса Экрана 3.
    insert_default_categories()

    print("FreelanceHub bot запущен.", flush=True)
    # infinity_polling сам оборачивает опрос Telegram в бесконечный цикл с
    # обработкой исключений, поэтому падение одного обработчика не останавливает бота.
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
