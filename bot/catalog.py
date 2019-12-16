from . import telegram_bot
from .utils import Access, Navigation, Helpers
from telebot.types import Message
from core import files
from resources import strings, keyboards


@telegram_bot.message_handler(content_types=['text'], func=Access.catalog)
def catalog_handler(message: Message):
    user_id = message.from_user.id

    root_categories = files.get_parent_categories()
    select_message = strings.get_string('catalog.categories.select')
    categories_keyboard = keyboards.from_categories_list_to_keyboard(root_categories)
    telegram_bot.send_message(user_id, select_message, reply_markup=categories_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(user_id, category_handler, current_category=None)


def category_handler(message: Message, *args, **kwargs):
    user_id = message.from_user.id

    def error():
        telegram_bot.send_message(user_id, strings.get_string('catalog.categories.select'))
        telegram_bot.register_next_step_handler_by_chat_id(user_id, category_handler)

    if not message.text:
        error()
        return
    if strings.get_string('back') in message.text:
        # Go back
        pass
    current_category = kwargs.get('current_category')
    category = files.get_category_by_name(message.text, current_category)
    if not category:
        error()
        return
    if category.file_set.count() > 0:
        for file in category.file_set.all():
            Helpers.send_file(user_id, file)
    if category.get_children().count() > 0:
        categories = category.get_children()
        select_message = strings.get_string('catalog.categories.select')
        categories_keyboard = keyboards.from_categories_list_to_keyboard(categories)
        telegram_bot.send_message(user_id, select_message, reply_markup=categories_keyboard)
    telegram_bot.register_next_step_handler_by_chat_id(user_id, category_handler, current_category=category)
