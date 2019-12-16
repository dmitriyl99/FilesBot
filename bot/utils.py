from . import telegram_bot
from telebot.types import Message
from core import users
from resources import strings, keyboards
from filebot.models import File
import os


class Access:
    @staticmethod
    def _auth(message: Message):
        user_id = message.from_user.id
        user = users.get_user_by_telegram_id(user_id)
        return user

    @staticmethod
    def _private(message: Message):
        return message.chat.type == 'private'

    @staticmethod
    def contacts(message: Message):
        if not message.text:
            return False
        return Access._private(message) and Access._auth(message) \
               and strings.get_string('main_menu.contacts') in message.text

    @staticmethod
    def share(message: Message):
        if not message.text:
            return False
        return Access._private(message) and Access._auth(message) and strings.get_string('main_menu.share') in message.text

    @staticmethod
    def catalog(m: Message):
        if not m.text:
            return False
        return Access._private(m) and Access._auth(m) and strings.get_string('main_menu.categories') in m.text


class Navigation:
    @staticmethod
    def to_main_menu(chat_id, message_text=None):
        if message_text:
            menu_message = message_text
        else:
            menu_message = strings.get_string('main_menu.menu')
        main_menu_keyboard = keyboards.get_keyboard('main_menu')
        telegram_bot.send_message(chat_id, menu_message, reply_markup=main_menu_keyboard, parse_mode='HTML')


class Helpers:
    @staticmethod
    def send_file(chat_id: int, file: File):
        if os.path.exists(file.file_path):
            extension = file.get_file_extension()
            if extension in ['jpg', 'png']:
                chat_action = 'sending_photo'
                method = telegram_bot.send_photo
            elif extension in ['mp3']:
                chat_action = 'sending_audio'
                method = telegram_bot.send_audio
            else:
                chat_action = 'sending_document'
                method = telegram_bot.send_document
            telegram_bot.send_chat_action(chat_id, chat_action)
            method(chat_id, open(file.file_path, 'rb'), caption=file.caption)
