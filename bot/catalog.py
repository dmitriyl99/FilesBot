from . import telegram_bot
from .utils import Access, Navigation, Helpers
from telebot.types import Message
from core import files, users
from resources import strings, keyboards


def _go_back(user_id, current_category):
    if not current_category:
        Navigation.to_main_menu(user_id)
        return
    if current_category.parent:
        catalog_message = strings.get_string('catalog.categories.select')
        categories_keyboard = keyboards.from_categories_list_to_keyboard(current_category.parent.get_children())
        telegram_bot.send_message(user_id, catalog_message, reply_markup=categories_keyboard)
        telegram_bot.register_next_step_handler_by_chat_id(user_id, category_handler,
                                                           current_category=current_category.parent)
        return
    else:
        Navigation.to_catalog(user_id)
        return


@telegram_bot.message_handler(content_types=['text'], func=Access.catalog)
def catalog_handler(message: Message):
    user_id = message.from_user.id

    Navigation.to_catalog(user_id)


def category_handler(message: Message, *args, **kwargs):
    user_id = message.from_user.id
    current_category = kwargs.get('current_category')

    def error():
        telegram_bot.send_message(user_id, strings.get_string('catalog.categories.select'))
        telegram_bot.register_next_step_handler_by_chat_id(user_id, category_handler, current_category=current_category)

    if not message.text:
        error()
        return
    if strings.get_string('back') in message.text:
        _go_back(user_id, current_category)
    else:
        category = files.get_category_by_name(message.text, current_category)
        if not category:
            error()
            return
        category.add_click()
        new_current_category = category if category.has_children else category.parent
        if category.file_set.count() > 0:
            category_files = category.file_set.all()
            select_message = strings.get_string('catalog.files.select')
            files_keyboard = keyboards.from_files_list_to_keyboard(category_files)
            telegram_bot.send_message(user_id, select_message, reply_markup=files_keyboard)
            telegram_bot.register_next_step_handler_by_chat_id(user_id, file_handler, current_category=category)
            return
        if category.get_children().count() > 0:
            categories = category.get_children()
            select_message = strings.get_string('catalog.categories.select')
            categories_keyboard = keyboards.from_categories_list_to_keyboard(categories)
            telegram_bot.send_message(user_id, select_message, reply_markup=categories_keyboard)
        telegram_bot.register_next_step_handler_by_chat_id(user_id, category_handler, current_category=new_current_category)


def file_handler(message: Message, *args, **kwargs):
    user_id = message.from_user.id
    current_category = kwargs.get('current_category')
    user = users.get_user_by_telegram_id(user_id)

    def error():
        telegram_bot.send_message(user_id, strings.get_string('catalog.files.select'))
        telegram_bot.register_next_step_handler_by_chat_id(user_id, file_handler,
                                                           current_category=current_category)

    if not message.text:
        error()
        return
    if strings.get_string('back') in message.text:
        _go_back(user_id, current_category)
    else:
        file = files.get_file_by_name(message.text)
        if not file:
            error()
            return
        Helpers.send_file(user_id, file, user)
        telegram_bot.register_next_step_handler_by_chat_id(user_id, file_handler,
                                                           current_category=current_category)
