START = "Добро пожаловать в FreelanceHub\nБиржа фриланс-заказов внутри Telegram"

MAIN_MENU = "Добро пожаловать в FreelanceHub\nВыберите кнопку из главного меню"
UNKNOWN_COMMAND = "Нераспознанная команда. Пожалуйста, нажмите выбранную кнопку в меню."

ASK_CATEGORY = "Создание заказа\nВыберите категорию"

ASK_DESCRIPTION = "Опишите, что нужно сделать\nОт 1 до 1000 символов"

ASK_BUDGET = "Укажите бюджет заказа\nВведите число и выберите валюту"
CURRENCY_UNAVAILABLE = "Не удалось получить курс валют. Попробуйте позже или укажите бюджет в рублях."

ASK_DEADLINE = "Укажите срок выполнения\nВведите дату и время в формате ДД.ММ.ГГГГ ЧЧ:ММ"


def order_preview(category_name: str, description: str, budget: float, currency: str, deadline_str: str) -> str:
    return (
        "Проверьте заказ перед публикацией\n"
        f"Категория: {category_name}\n"
        f"Описание: {description}\n"
        f"Бюджет: {budget:g} {currency}\n"
        f"Срок: {deadline_str}"
    )


ORDER_PUBLISHED = "Заказ опубликован."


def order_card(index: int, total: int, category_name: str, description: str,
                budget_rub: float, deadline_str: str) -> str:
    return (
        f"Заказ {index} из {total}\n"
        f"Категория: {category_name}\n"
        f"Описание: {description}\n"
        f"Бюджет: {budget_rub:g} RUB\n"
        f"Срок: {deadline_str}"
    )


NO_OPEN_ORDERS = "Сейчас нет доступных заказов. Загляните позже."
END_OF_LIST = "Больше заказов нет"


def response_menu(price_text: str, comment_text: str, media_count: int) -> str:
    return (
        "Отклик на заказ\n"
        f"Цена: {price_text}\n"
        f"Комментарий: {comment_text}\n"
        f"Медиафайлы: {media_count} прикреплено"
    )


RESPONSE_SENT = "Отклик отправлен."
NEED_PRICE_FIRST = "Сначала укажите цену."
CANNOT_RESPOND_OWN_ORDER = "Нельзя откликнуться на свой заказ."
ALREADY_RESPONDED = "Вы уже откликались на этот заказ."

ASK_PRICE = "Укажите вашу цену за выполнение заказа"
PRICE_INVALID = "Цена должна быть положительным числом."

ASK_COMMENT = "Добавьте комментарий к отклику\nНеобязательно, до 500 символов"
COMMENT_TOO_LONG = "Комментарий не должен превышать 500 символов. Сократите текст и попробуйте ещё раз."

ASK_MEDIA = "Прикрепите медиафайлы\nОтправьте одно или несколько изображений/файлов"

GENERIC_ERROR = "Что-то пошло не так. Попробуйте ещё раз или вернитесь в главное меню."
UNDER_DEVELOPMENT = "Этот раздел ещё в разработке. Скоро будет доступен."
