from telebot import types

from ui import texts, keyboards
from ui.states import States, StateStorage
from repositories.user_repository import UserRepository
from repositories.category_repository import CategoryRepository
from repositories.order_repository import OrderRepository
from repositories.response_repository import ResponseRepository
from repositories.review_repository import ReviewRepository
from services.currency_service import CurrencyService
from services.order_service import OrderService, OrderValidationError
from services.response_service import ResponseService, ResponseValidationError
from services.rating_service import RatingService
from api.currency_api import CurrencyApiClient


def _services_for_session(session, currency_api_client: CurrencyApiClient):
    user_repo = UserRepository(session)
    category_repo = CategoryRepository(session)
    order_repo = OrderRepository(session)
    response_repo = ResponseRepository(session)
    review_repo = ReviewRepository(session)

    currency_service = CurrencyService(currency_api_client)
    order_service = OrderService(order_repo, category_repo, currency_service)
    response_service = ResponseService(response_repo, order_repo)
    rating_service = RatingService(review_repo)

    return {
        "user_repo": user_repo,
        "order_service": order_service,
        "response_service": response_service,
        "rating_service": rating_service,
    }


def register_handlers(bot, db, currency_api_client: CurrencyApiClient, support_username: str):
    state_storage = StateStorage()

    def current_user(message, services):
        tg = message.from_user
        full_name = tg.full_name or tg.username or str(tg.id)
        return services["user_repo"].get_or_create(tg.id, tg.username, full_name)

    def show_main_menu(chat_id, telegram_id):
        state_storage.clear(telegram_id)
        state_storage.set_state(telegram_id, States.MAIN_MENU)
        bot.send_message(chat_id, texts.MAIN_MENU, reply_markup=keyboards.main_menu_kb())

    @bot.message_handler(commands=["start"])
    def handle_start(message):
        bot.send_message(message.chat.id, texts.START, reply_markup=keyboards.start_kb())
        state_storage.clear(message.from_user.id)

    @bot.message_handler(func=lambda m: m.text == "Старт")
    def handle_start_button(message):
        session = db.get_session()
        try:
            services = _services_for_session(session, currency_api_client)
            current_user(message, services)
        finally:
            session.close()
        show_main_menu(message.chat.id, message.from_user.id)

    @bot.message_handler(func=lambda m: m.text == "В главное меню")
    def handle_back_to_menu(message):
        show_main_menu(message.chat.id, message.from_user.id)

    @bot.message_handler(func=lambda m: m.text == "Создать заказ")
    def handle_create_order_entry(message):
        session = db.get_session()
        try:
            services = _services_for_session(session, currency_api_client)
            categories = services["order_service"].get_categories()
            state_storage.set_state(message.from_user.id, States.CREATE_ORDER_CATEGORY)
            bot.send_message(message.chat.id, texts.ASK_CATEGORY, reply_markup=keyboards.categories_kb(categories))
        finally:
            session.close()

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.CREATE_ORDER_CATEGORY)
    def handle_category_choice(message):
        telegram_id = message.from_user.id
        if message.text == "Назад":
            show_main_menu(message.chat.id, telegram_id)
            return

        session = db.get_session()
        try:
            services = _services_for_session(session, currency_api_client)
            categories = {c.name: c for c in services["order_service"].get_categories()}
            category = categories.get(message.text)
            if category is None:
                bot.send_message(message.chat.id, texts.UNKNOWN_COMMAND)
                return
            state_storage.update_data(telegram_id, category_id=category.id, category_name=category.name)
        finally:
            session.close()

        state_storage.set_state(telegram_id, States.CREATE_ORDER_DESCRIPTION)
        bot.send_message(message.chat.id, texts.ASK_DESCRIPTION, reply_markup=keyboards.back_only_kb())

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.CREATE_ORDER_DESCRIPTION)
    def handle_description(message):
        telegram_id = message.from_user.id
        if message.text == "Назад":
            handle_create_order_entry(message)
            return

        session = db.get_session()
        try:
            services = _services_for_session(session, currency_api_client)
            try:
                description = services["order_service"].validate_description(message.text)
            except OrderValidationError as exc:
                bot.send_message(message.chat.id, str(exc))
                return
        finally:
            session.close()

        state_storage.update_data(telegram_id, description=description)
        state_storage.set_state(telegram_id, States.CREATE_ORDER_BUDGET_CURRENCY)
        bot.send_message(message.chat.id, texts.ASK_BUDGET, reply_markup=keyboards.currency_kb())

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.CREATE_ORDER_BUDGET_CURRENCY)
    def handle_currency_choice(message):
        telegram_id = message.from_user.id
        if message.text == "Назад":
            state_storage.set_state(telegram_id, States.CREATE_ORDER_DESCRIPTION)
            bot.send_message(message.chat.id, texts.ASK_DESCRIPTION, reply_markup=keyboards.back_only_kb())
            return
        if message.text not in ("RUB", "USD", "EUR"):
            bot.send_message(message.chat.id, texts.UNKNOWN_COMMAND)
            return

        state_storage.update_data(telegram_id, currency=message.text)
        state_storage.set_state(telegram_id, States.CREATE_ORDER_BUDGET_AMOUNT)
        bot.send_message(message.chat.id, texts.ASK_BUDGET, reply_markup=keyboards.back_only_kb())

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.CREATE_ORDER_BUDGET_AMOUNT)
    def handle_budget_amount(message):
        telegram_id = message.from_user.id
        if message.text == "Назад":
            state_storage.set_state(telegram_id, States.CREATE_ORDER_BUDGET_CURRENCY)
            bot.send_message(message.chat.id, texts.ASK_BUDGET, reply_markup=keyboards.currency_kb())
            return

        data = state_storage.get_data(telegram_id)
        session = db.get_session()
        try:
            services = _services_for_session(session, currency_api_client)
            order_service = services["order_service"]
            try:
                budget = order_service.validate_budget(message.text)
                budget_rub = order_service.calculate_budget_rub(budget, data["currency"])
            except OrderValidationError as exc:
                bot.send_message(message.chat.id, str(exc))
                return
        finally:
            session.close()

        state_storage.update_data(telegram_id, budget=budget, budget_rub=budget_rub)
        state_storage.set_state(telegram_id, States.CREATE_ORDER_DEADLINE)
        bot.send_message(message.chat.id, texts.ASK_DEADLINE, reply_markup=keyboards.back_only_kb())

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.CREATE_ORDER_DEADLINE)
    def handle_deadline(message):
        telegram_id = message.from_user.id
        if message.text == "Назад":
            state_storage.set_state(telegram_id, States.CREATE_ORDER_BUDGET_AMOUNT)
            bot.send_message(message.chat.id, texts.ASK_BUDGET, reply_markup=keyboards.back_only_kb())
            return

        session = db.get_session()
        try:
            services = _services_for_session(session, currency_api_client)
            try:
                deadline = services["order_service"].validate_deadline(message.text)
            except OrderValidationError as exc:
                bot.send_message(message.chat.id, str(exc))
                return
        finally:
            session.close()

        data = state_storage.get_data(telegram_id)
        state_storage.update_data(telegram_id, deadline=deadline)
        state_storage.set_state(telegram_id, States.CREATE_ORDER_CONFIRM)
        preview = texts.order_preview(
            data["category_name"], data["description"], data["budget"], data["currency"],
            deadline.strftime("%d.%m.%Y %H:%M"),
        )
        bot.send_message(message.chat.id, preview, reply_markup=keyboards.order_preview_kb())

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.CREATE_ORDER_CONFIRM)
    def handle_order_confirm(message):
        telegram_id = message.from_user.id
        if message.text == "Назад":
            state_storage.set_state(telegram_id, States.CREATE_ORDER_DEADLINE)
            bot.send_message(message.chat.id, texts.ASK_DEADLINE, reply_markup=keyboards.back_only_kb())
            return
        if message.text != "Опубликовать":
            bot.send_message(message.chat.id, texts.UNKNOWN_COMMAND)
            return

        data = state_storage.get_data(telegram_id)
        session = db.get_session()
        try:
            services = _services_for_session(session, currency_api_client)
            user = current_user(message, services)
            services["order_service"].publish_order(
                client_id=user.id, category_id=data["category_id"], description=data["description"],
                budget=data["budget"], currency=data["currency"], budget_rub=data["budget_rub"],
                deadline=data["deadline"],
            )
        finally:
            session.close()

        bot.send_message(message.chat.id, texts.ORDER_PUBLISHED)
        show_main_menu(message.chat.id, telegram_id)

    @bot.message_handler(func=lambda m: m.text == "Лента заказов")
    def handle_feed_entry(message):
        telegram_id = message.from_user.id
        session = db.get_session()
        try:
            services = _services_for_session(session, currency_api_client)
            user = current_user(message, services)
            orders = services["order_service"].get_feed(user.id)
        finally:
            session.close()

        if not orders:
            bot.send_message(message.chat.id, texts.NO_OPEN_ORDERS, reply_markup=keyboards.to_main_menu_kb())
            return

        order_ids = [o.id for o in orders]
        state_storage.set_state(telegram_id, States.FEED_BROWSING)
        state_storage.update_data(telegram_id, feed_order_ids=order_ids, feed_index=0)
        _show_feed_card(message.chat.id, telegram_id)

    def _show_feed_card(chat_id, telegram_id):
        data = state_storage.get_data(telegram_id)
        order_ids = data["feed_order_ids"]
        index = data["feed_index"]

        if index >= len(order_ids):
            bot.send_message(chat_id, texts.END_OF_LIST, reply_markup=keyboards.to_main_menu_kb())
            return

        session = db.get_session()
        try:
            services = _services_for_session(session, currency_api_client)
            order = services["order_service"].get_order(order_ids[index])
            categories = {c.id: c.name for c in services["order_service"].get_categories()}
        finally:
            session.close()

        card_text = texts.order_card(
            index + 1, len(order_ids), categories.get(order.category_id, "—"),
            order.description, float(order.budget_rub), order.deadline.strftime("%d.%m.%Y %H:%M"),
        )
        kb = keyboards.feed_kb(has_prev=index > 0, has_next=index < len(order_ids) - 1)
        bot.send_message(chat_id, card_text, reply_markup=kb)

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.FEED_BROWSING)
    def handle_feed_navigation(message):
        telegram_id = message.from_user.id
        data = state_storage.get_data(telegram_id)

        if message.text == "В главное меню":
            show_main_menu(message.chat.id, telegram_id)
            return
        if message.text == "Дальше":
            state_storage.update_data(telegram_id, feed_index=data["feed_index"] + 1)
            _show_feed_card(message.chat.id, telegram_id)
            return
        if message.text == "Назад" and data["feed_index"] > 0:
            state_storage.update_data(telegram_id, feed_index=data["feed_index"] - 1)
            _show_feed_card(message.chat.id, telegram_id)
            return
        if message.text == "Откликнуться":
            order_id = data["feed_order_ids"][data["feed_index"]]
            state_storage.update_data(telegram_id, response_order_id=order_id, response_price=None,
                                       response_comment=None, response_media=[])
            state_storage.set_state(telegram_id, States.RESPONSE_MENU)
            _show_response_menu(message.chat.id, telegram_id)
            return

        bot.send_message(message.chat.id, texts.UNKNOWN_COMMAND)

    def _show_response_menu(chat_id, telegram_id):
        data = state_storage.get_data(telegram_id)
        price_text = f"{data['response_price']:g}" if data.get("response_price") else "не указана"
        comment_text = data.get("response_comment") or "не указан"
        media_count = len(data.get("response_media", []))
        bot.send_message(chat_id, texts.response_menu(price_text, comment_text, media_count),
                          reply_markup=keyboards.response_menu_kb())

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.RESPONSE_MENU)
    def handle_response_menu(message):
        telegram_id = message.from_user.id
        text = message.text

        if text == "Назад":
            state_storage.set_state(telegram_id, States.FEED_BROWSING)
            _show_feed_card(message.chat.id, telegram_id)
            return
        if text == "Указать цену":
            state_storage.set_state(telegram_id, States.RESPONSE_PRICE)
            bot.send_message(message.chat.id, texts.ASK_PRICE, reply_markup=keyboards.back_only_kb())
            return
        if text == "Указать комментарий":
            state_storage.set_state(telegram_id, States.RESPONSE_COMMENT)
            bot.send_message(message.chat.id, texts.ASK_COMMENT, reply_markup=keyboards.back_only_kb())
            return
        if text == "Прикрепить медиафайлы":
            state_storage.set_state(telegram_id, States.RESPONSE_MEDIA)
            bot.send_message(message.chat.id, texts.ASK_MEDIA, reply_markup=keyboards.media_kb())
            return
        if text == "Отправить отклик":
            data = state_storage.get_data(telegram_id)
            if not data.get("response_price"):
                bot.send_message(message.chat.id, texts.NEED_PRICE_FIRST)
                return

            session = db.get_session()
            try:
                services = _services_for_session(session, currency_api_client)
                user = current_user(message, services)
                try:
                    services["response_service"].submit_response(
                        order_id=data["response_order_id"], executor_id=user.id,
                        price=data["response_price"], comment=data.get("response_comment"),
                        media_file_ids=data.get("response_media", []),
                    )
                except ResponseValidationError as exc:
                    bot.send_message(message.chat.id, str(exc))
                    return
            finally:
                session.close()

            bot.send_message(message.chat.id, texts.RESPONSE_SENT)
            show_main_menu(message.chat.id, telegram_id)
            return

        bot.send_message(message.chat.id, texts.UNKNOWN_COMMAND)

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.RESPONSE_PRICE)
    def handle_response_price(message):
        telegram_id = message.from_user.id
        if message.text == "Назад":
            state_storage.set_state(telegram_id, States.RESPONSE_MENU)
            _show_response_menu(message.chat.id, telegram_id)
            return

        session = db.get_session()
        try:
            services = _services_for_session(session, currency_api_client)
            try:
                price = services["response_service"].validate_price(message.text)
            except ResponseValidationError as exc:
                bot.send_message(message.chat.id, str(exc))
                return
        finally:
            session.close()

        state_storage.update_data(telegram_id, response_price=price)
        state_storage.set_state(telegram_id, States.RESPONSE_MENU)
        _show_response_menu(message.chat.id, telegram_id)

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.RESPONSE_COMMENT)
    def handle_response_comment(message):
        telegram_id = message.from_user.id
        if message.text == "Назад":
            state_storage.set_state(telegram_id, States.RESPONSE_MENU)
            _show_response_menu(message.chat.id, telegram_id)
            return

        session = db.get_session()
        try:
            services = _services_for_session(session, currency_api_client)
            try:
                comment = services["response_service"].validate_comment(message.text)
            except ResponseValidationError as exc:
                bot.send_message(message.chat.id, str(exc))
                return
        finally:
            session.close()

        state_storage.update_data(telegram_id, response_comment=comment)
        state_storage.set_state(telegram_id, States.RESPONSE_MENU)
        _show_response_menu(message.chat.id, telegram_id)

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.RESPONSE_MEDIA,
                          content_types=["photo", "document"])
    def handle_response_media_file(message):
        telegram_id = message.from_user.id
        file_id = message.photo[-1].file_id if message.photo else message.document.file_id
        data = state_storage.get_data(telegram_id)
        media = data.get("response_media", [])
        media.append(file_id)
        state_storage.update_data(telegram_id, response_media=media)
        bot.send_message(
            message.chat.id,
            f"{texts.ASK_MEDIA}\nПрикреплено: {len(media)} файл(ов)",
            reply_markup=keyboards.media_kb(),
        )

    @bot.message_handler(func=lambda m: state_storage.get_state(m.from_user.id) == States.RESPONSE_MEDIA)
    def handle_response_media_buttons(message):
        telegram_id = message.from_user.id
        if message.text in ("Готово", "Назад"):
            state_storage.set_state(telegram_id, States.RESPONSE_MENU)
            _show_response_menu(message.chat.id, telegram_id)
            return
        bot.send_message(message.chat.id, texts.UNKNOWN_COMMAND)

    @bot.message_handler(func=lambda m: m.text in ("Мои заказы", "Профиль"))
    def handle_not_implemented_yet(message):
        bot.send_message(message.chat.id, texts.UNDER_DEVELOPMENT, reply_markup=keyboards.main_menu_kb())

    @bot.message_handler(content_types=["photo", "document", "voice", "video", "sticker", "audio"])
    def handle_unsupported_content(message):
        pass

    @bot.message_handler(func=lambda m: True)
    def handle_fallback(message):
        bot.send_message(message.chat.id, texts.UNKNOWN_COMMAND, reply_markup=keyboards.main_menu_kb())
