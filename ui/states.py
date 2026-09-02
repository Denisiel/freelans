class States:
    MAIN_MENU = "main_menu"
    CREATE_ORDER_CATEGORY = "create_order_category"
    CREATE_ORDER_DESCRIPTION = "create_order_description"
    CREATE_ORDER_BUDGET_CURRENCY = "create_order_budget_currency"
    CREATE_ORDER_BUDGET_AMOUNT = "create_order_budget_amount"
    CREATE_ORDER_DEADLINE = "create_order_deadline"
    CREATE_ORDER_CONFIRM = "create_order_confirm"
    FEED_BROWSING = "feed_browsing"
    RESPONSE_MENU = "response_menu"
    RESPONSE_PRICE = "response_price"
    RESPONSE_COMMENT = "response_comment"
    RESPONSE_MEDIA = "response_media"


class StateStorage:
    def __init__(self):
        self._states = {}
        self._data = {}

    def get_state(self, telegram_id: int):
        return self._states.get(telegram_id, States.MAIN_MENU)

    def set_state(self, telegram_id: int, state: str):
        self._states[telegram_id] = state

    def get_data(self, telegram_id: int) -> dict:
        return self._data.setdefault(telegram_id, {})

    def update_data(self, telegram_id: int, **kwargs):
        self.get_data(telegram_id).update(kwargs)

    def clear(self, telegram_id: int):
        self._states.pop(telegram_id, None)
        self._data.pop(telegram_id, None)
