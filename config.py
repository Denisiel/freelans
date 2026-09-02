import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///freelancehub.db")

CURRENCY_API_KEY = os.getenv("CURRENCY_API_KEY", "")
CURRENCY_API_URL = os.getenv("CURRENCY_API_URL", "https://api.currencyapi.com/v3/latest")

SUPPORT_USERNAME = os.getenv("SUPPORT_USERNAME", "@freelancehub_support")

if not BOT_TOKEN:
    raise RuntimeError(
        "BOT_TOKEN не задан. Создайте файл .env на основе .env.example "
        "и укажите токен бота, полученный у @BotFather."
    )
