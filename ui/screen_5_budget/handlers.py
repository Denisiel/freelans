"""Обработчики выбора валюты и ввода суммы бюджета заказа."""

from telebot import types
from telebot.states.sync.context import StateContext

from bot_instance import bot
from services.order_service import calculate_budget_rub, validate_budget
from ui.common import send_screen
from ui.screen_5_budget.keyboards import get_back_only_keyboard, get_screen_5_currency_keyboard
from ui.screen_5_budget.texts import BUDGET_INVALID_TEXT, CURRENCY_UNAVAILABLE_TEXT, get_screen_5_budget_text
from ui.states import OrderStates


def show_screen_5_currency(chat_id: int, state: StateContext):
    """Показывает выбор валюты — первый шаг указания бюджета."""

    state.set(OrderStates.screen_5_currency)
    send_screen(chat_id, state, get_screen_5_budget_text(), get_screen_5_currency_keyboard())


def show_screen_5_budget_amount(chat_id: int, state: StateContext):
    """Запрашивает саму сумму бюджета после выбора валюты."""

    state.set(OrderStates.screen_5_budget_amount)
    bot.send_message(chat_id, get_screen_5_budget_text(), reply_markup=get_back_only_keyboard())


@bot.callback_query_handler(func=lambda call: call.data.startswith("currency:"), state=OrderStates.screen_5_currency)
def callback_screen_5_currency_handler(call: types.CallbackQuery, state: StateContext):
    """Сохраняет выбранную валюту и переходит к вводу суммы."""

    bot.answer_callback_query(call.id)
    action = call.data.split(":", 1)[1]

    if action == "back":
        from ui.screen_4_description.handlers import show_screen_4_description

        show_screen_4_description(call.message.chat.id, state)
        return

    state.add_data(currency=action)
    show_screen_5_budget_amount(call.message.chat.id, state)


@bot.message_handler(state=OrderStates.screen_5_budget_amount)
def message_screen_5_budget_amount_handler(message: types.Message, state: StateContext):
    """Проверяет сумму, пересчитывает её в рубли и переходит к сроку заказа."""

    if message.text == "Назад":
        show_screen_5_currency(message.chat.id, state)
        return

    budget = validate_budget(message.text)
    if budget is None:
        bot.send_message(message.chat.id, BUDGET_INVALID_TEXT)
        return

    with state.data() as data:
        currency = data["currency"]

    try:
        # Курс запрашивается у внешнего API и может быть временно недоступен.
        budget_rub = calculate_budget_rub(budget, currency)
    except Exception:
        bot.send_message(message.chat.id, CURRENCY_UNAVAILABLE_TEXT)
        return

    state.add_data(budget=budget, budget_rub=budget_rub)

    from ui.screen_6_deadline.handlers import show_screen_6_deadline

    show_screen_6_deadline(message.chat.id, state)
