"""
Handlers for start bot
"""

from . import telegram_bot
from core import users, settings
from telebot.types import Message
from resources import strings, keyboards
from .utils import Navigation


@telegram_bot.message_handler(commands=['start'])
def start_handler(message: Message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    username = message.from_user.username

    users.add_user(user_id, first_name, last_name, username)

    bot_settings = settings.get_settings()
    if not bot_settings:
        telegram_bot.send_message(chat_id, strings.get_string('main_menu.no_start_message'))
        return
    start_message = bot_settings.start_message_text
    Navigation.to_main_menu(chat_id, start_message)
