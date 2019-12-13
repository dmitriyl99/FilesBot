from . import telegram_bot
from telebot.types import Message
from core import users
from resources import strings, keyboards


class Access:
    @staticmethod
    def _auth(message: Message):
        user_id = message.from_user.id
        user = users.get_user_by_telegram_id(user_id)
        return user

    @staticmethod
    def _private(message: Message):
        return message.chat.type == 'private'


class Navigation:
    @staticmethod
    def to_main_menu(chat_id, message_text=None):
        if message_text:
            menu_message = message_text
        else:
            menu_message = strings.get_string('main_menu.menu')
        main_menu_keyboard = keyboards.get_keyboard('main_menu')
        telegram_bot.send_message(chat_id, menu_message, reply_markup=main_menu_keyboard, parse_mode='HTML')
