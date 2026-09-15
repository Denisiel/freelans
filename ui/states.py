"""Состояния конечного автомата, описывающего навигацию по экранам бота."""

from telebot.states import State, StatesGroup


class OrderStates(StatesGroup):
    """Все возможные этапы диалога пользователя с FreelanceHub.

    Состояние хранится отдельно для каждого пользователя/чата и определяет,
    какой обработчик должен принять следующее сообщение или нажатие кнопки.
    Номер в имени соответствует номеру экрана в сценарии из ТЗ.
    """

    screen_2_main_menu = State()

    # Экраны 3-7: пошаговое создание заказа.
    screen_3_category = State()
    screen_4_description = State()
    screen_5_currency = State()
    screen_5_budget_amount = State()
    screen_6_deadline = State()
    screen_7_confirm = State()

    # Экран 8: лента открытых заказов.
    screen_8_feed = State()

    # Экран 9 и его подэкраны: конструктор отклика на заказ.
    screen_9_menu = State()
    screen_9_price = State()
    screen_9_comment = State()
    screen_9_media = State()

    # Экраны 10-11: список своих заказов/откликов и карточка заказа.
    screen_10_my_orders = State()
    screen_11_order_card = State()
