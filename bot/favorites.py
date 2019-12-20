from . import telegram_bot
from telebot.types import CallbackQuery
from core import users, files
from resources import strings, keyboards


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
