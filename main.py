import logging

import telebot
from telebot import ExceptionHandler

import config
from repositories.database import Database, DatabaseConnectionError
from repositories.category_repository import CategoryRepository
from api.currency_api import CurrencyApiClient
from ui.handlers import register_handlers

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("freelancehub")


class BotErrorHandler(ExceptionHandler):
    def handle(self, exception):
        logger.exception("Необработанная ошибка в обработчике: %s", exception)
        return True


def main():
    try:
        db = Database(config.DATABASE_URL)
        db.create_all_tables()
    except DatabaseConnectionError as exc:
        logger.critical("Не удалось подключиться к базе данных: %s", exc)
        raise SystemExit(1)

    session = db.get_session()
    try:
        CategoryRepository(session).seed_default_categories()
    finally:
        session.close()

    currency_api_client = CurrencyApiClient(
        api_key=config.CURRENCY_API_KEY,
        base_url=config.CURRENCY_API_URL,
    )

    bot = telebot.TeleBot(config.BOT_TOKEN, exception_handler=BotErrorHandler())
    register_handlers(bot, db, currency_api_client, config.SUPPORT_USERNAME)

    logger.info("FreelanceHub bot запущен.")
    bot.infinity_polling(skip_pending=True)


if __name__ == "__main__":
    main()
