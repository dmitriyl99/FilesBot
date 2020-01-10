from . import telegram_bot
from telebot.types import Message
from telebot.apihelper import ApiException
from core import users, files
from resources import strings, keyboards
from filebot.models import File, BotUser
from shutil import copyfile
import os
from time import sleep


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

    @staticmethod
    def upload(m: Message):
        if not m.text:
            return False
        return Access._private(m) and Access._auth(m) and strings.get_string('main_menu.upload') in m.text

    @staticmethod
    def favorites(m: Message):
        if not m.text:
            return False
        return Access._private(m) and Access._auth(m) and strings.get_string('main_menu.favorites') in m.text

    @staticmethod
    def search(m: Message):
        if not m.text:
            return False
        return Access._private(m) and Access._auth(m) and strings.get_string('main_menu.search') in m.text

    @staticmethod
    def empty(m: Message):
        return Access._private(m) and Access._auth(m)


class Navigation:
    @staticmethod
    def to_main_menu(chat_id, message_text=None):
        if message_text:
            menu_message = message_text
        else:
            menu_message = strings.get_string('main_menu.menu')
        main_menu_keyboard = keyboards.get_keyboard('main_menu')
        telegram_bot.send_message(chat_id, menu_message, reply_markup=main_menu_keyboard, parse_mode='HTML')

    @staticmethod
    def to_catalog(chat_id):
        from bot.catalog import category_handler
        root_categories = files.get_parent_categories()
        if not root_categories:
            empty_message = strings.get_string('catalog.categories.empty')
            telegram_bot.send_message(chat_id, empty_message)
            return
        select_message = strings.get_string('catalog.categories.select')
        categories_keyboard = keyboards.from_categories_list_to_keyboard(root_categories, include_from_users=True)
        telegram_bot.send_message(chat_id, select_message, reply_markup=categories_keyboard)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, category_handler, current_category=None,
                                                           keyboard=categories_keyboard)

    @staticmethod
    def to_search(chat_id):
        from .search import search_handler
        index_message = strings.get_string('search.type_query')
        search_keyboard = keyboards.get_keyboard('search.index')
        telegram_bot.send_message(chat_id, index_message, reply_markup=search_keyboard)
        telegram_bot.register_next_step_handler_by_chat_id(chat_id, search_handler)


class Helpers:
    @staticmethod
    def send_file(chat_id: int, file: File, user: BotUser, favorites=False):
        file_path = file.file_path
        if file.hide_file_name or file.unprintable_file_name:
            template_file_name = 'SendSoundBot' if file.hide_file_name else 'Цензура'
            template_file_name += file.extension
            template_file_path = os.path.join(os.path.dirname(file.file_path), template_file_name)
            copyfile(file.file_path, template_file_path)
            file_path = template_file_path
        if os.path.exists(file_path):
            extension = file.get_file_extension()
            if extension in ['.jpg', '.png']:
                chat_action = 'upload_photo'
                method = telegram_bot.send_photo
            elif extension in ['.mp3']:
                chat_action = 'upload_audio'
                method = telegram_bot.send_audio
            else:
                chat_action = 'upload_document'
                method = telegram_bot.send_document
            file_keyboard = keyboards.from_file_to_inline_keyboard_favorite(file,
                                                                            remove=user.favorite_file_exists(file)
                                                                            if not favorites else True)
            telegram_bot.send_chat_action(chat_id, chat_action)
            method(chat_id, open(file_path, 'rb'), caption=file.caption,
                   reply_markup=file_keyboard, parse_mode='HTML')
            if file.hide_file_name or file.unprintable_file_name:
                os.remove(file_path)

    @staticmethod
    def check_for_start_command(message: Message):
        return '/start' in message.text

    @staticmethod
    def distribute_advertising_post(text: str, file_path: str = None):
        all_users = users.get_all_users()
        file_id = None
        for user in all_users:
            if file_path:
                extension = os.path.splitext(os.path.basename(file_path))[1]
                if extension in ['.jpg', '.png']:
                    method = telegram_bot.send_photo
                elif extension in ['.mp3']:
                    method = telegram_bot.send_audio
                else:
                    method = telegram_bot.send_document
                try:
                    if file_id:
                        method(user.id, file_id, caption=text, parse_mode='HTML')
                    else:
                        message = method(user.id, open(file_path, 'rb'), caption=text, parse_mode='HTML')
                        file = message.document or message.audio or message.photo[-1]
                        file_id = file.file_id
                except Exception:
                    continue
            else:
                try:
                    telegram_bot.send_message(user.id, text, parse_mode='HTML')
                except ApiException:
                    continue
            sleep(0.1)
