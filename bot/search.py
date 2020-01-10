from . import telegram_bot
from .utils import Access, Navigation, Helpers
from telebot.types import Message
from telebot.apihelper import ApiException
from resources import strings, keyboards
from core import files, users


@telegram_bot.message_handler(content_types=['text'], func=Access.search)
def search_index(message: Message):
    user_id = message.from_user.id
    Navigation.to_search(user_id)


def search_handler(message: Message):
    user_id = message.from_user.id

    def error():
        error_message = strings.get_string('search.type_query')
        telegram_bot.send_message(user_id, error_message)
        telegram_bot.register_next_step_handler_by_chat_id(user_id, search_handler)

    def not_found():
        not_found_message = strings.get_string('search.not_found')
        telegram_bot.send_message(user_id, not_found_message)
        telegram_bot.register_next_step_handler_by_chat_id(user_id, search_handler)

    if not message.text:
        error()
        return
    if Helpers.check_for_start_command(message):
        Navigation.to_main_menu(user_id)
        return
    if strings.get_string('back') in message.text:
        Navigation.to_main_menu(user_id)
        return
    found_files = files.search_files(message.text)
    if not found_files:
        not_found()
        return
    files_keyboard = keyboards.from_files_list_to_keyboard(found_files)
    select_message = strings.get_string('catalog.files.select')
    try:
        telegram_bot.send_message(user_id, select_message, reply_markup=files_keyboard)
    except ApiException:
        telegram_bot.send_message(user_id, strings.get_string('search.refine'))
        telegram_bot.register_next_step_handler_by_chat_id(user_id, search_handler)
    else:
        telegram_bot.register_next_step_handler_by_chat_id(user_id, file_handler)


def file_handler(message: Message):
    user_id = message.from_user.id
    user = users.get_user_by_telegram_id(user_id)

    def error():
        telegram_bot.send_message(user_id, strings.get_string('catalog.files.select'))
        telegram_bot.register_next_step_handler_by_chat_id(user_id, file_handler)

    if not message.text:
        error()
        return
    if Helpers.check_for_start_command(message):
        Navigation.to_main_menu(user_id)
        return
    if strings.get_string('back') in message.text:
        Navigation.to_search(user_id)
    else:
        file = files.get_file_by_name(message.text)
        if not file:
            error()
            return
        Helpers.send_file(user_id, file, user)
        telegram_bot.register_next_step_handler_by_chat_id(user_id, file_handler)
