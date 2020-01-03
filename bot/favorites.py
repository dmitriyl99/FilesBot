from . import telegram_bot
from telebot.types import CallbackQuery, Message
from core import users, files
from resources import strings, keyboards
from .utils import Access, Helpers, Navigation


@telegram_bot.callback_query_handler(func=lambda m: True)
def favorite_query_handler(query: CallbackQuery):
    user_id = query.from_user.id
    user = users.get_user_by_telegram_id(user_id)

    def error(string_code):
        telegram_bot.answer_callback_query(query.id, strings.get_string(string_code),
                                           show_alert=True)

    if not user:
        error('catalog.add_favorite.not_allowed')
        return

    if not query.data.isnumeric():
        error('catalog.add_favorite.error')
        return
    file_id = int(query.data)
    file = files.get_file_by_id(file_id)
    if not file:
        error('catalog.add_favorite.error')
        return
    if file in user.favorites_files.all():
        user.favorites_files.remove(file)
        success_message = strings.get_string('catalog.add_favorite.removed')
        new_keyboard = keyboards.from_file_to_inline_keyboard_favorite(file)
    else:
        user.favorites_files.add(file)
        success_message = strings.get_string('catalog.add_favorite.added')
        new_keyboard = keyboards.from_file_to_inline_keyboard_favorite(file, remove=True)
    telegram_bot.answer_callback_query(query.id, success_message)
    telegram_bot.edit_message_reply_markup(user_id, query.message.message_id, query.inline_message_id, new_keyboard)


@telegram_bot.message_handler(content_types=['text'], func=Access.favorites)
def favorites_handler(message: Message):
    user_id = message.from_user.id
    user = users.get_user_by_telegram_id(user_id)

    user_files = user.favorites_files.all()
    if not user_files:
        empty_message = strings.get_string('favorites.empty')
        telegram_bot.send_message(user_id, empty_message)
        return
    select_message = strings.get_string('catalog.files.select')
    files_keyboard = keyboards.from_files_list_to_keyboard(user_files)
    telegram_bot.send_message(user_id, select_message, reply_markup=files_keyboard)
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
        Navigation.to_main_menu(user_id)
    else:
        file = files.get_file_by_name(message.text)
        if not file:
            error()
            return
        Helpers.send_file(user_id, file, user)
        telegram_bot.register_next_step_handler_by_chat_id(user_id, file_handler)
