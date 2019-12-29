from . import telegram_bot
from .utils import Access, Navigation
from telebot.types import Message
from resources import strings, keyboards
from filebot.models import File
from FileTelegramBot.settings import API_TOKEN
from django.core.files.storage import FileSystemStorage
import logging
import requests
import os
from core import users, files
import secrets


@telegram_bot.message_handler(content_types=['text'], func=Access.upload)
def index_handler(message: Message):
    user_id = message.from_user.id
    helper_text = strings.get_string('user_files.help_text')
    telegram_bot.send_message(user_id, helper_text)


@telegram_bot.message_handler(content_types=['audio', 'document'])
def user_file_handler(message: Message):
    if message.audio:
        user_telegram_file = message.audio
    elif message.document:
        user_telegram_file = message.document
    else:
        return
    if message.document and message.document.mime_type != 'audio/mpeg':
        return
    telegram_bot.send_audio(message.chat.id, user_telegram_file.file_id)
    file_size_mb = user_telegram_file.file_size / 1024 ** 2
    if file_size_mb > 1:
        too_much_size_message = strings.get_string('user_files.too_much_size')
        telegram_bot.reply_to(message, too_much_size_message)
    else:
        try:
            wait_message = strings.get_string('user_files.wait')
            telegram_bot.reply_to(message, wait_message)
            telegram_file_info = telegram_bot.get_file(user_telegram_file.file_id)
            telegram_file_path = telegram_file_info.file_path
            if message.audio:
                file_caption = user_telegram_file.title or user_telegram_file.performer
                if not file_caption:
                    file_caption = 'audio_' + secrets.token_hex(5)
            elif message.document:
                file_caption = user_telegram_file.file_name
            else:
                file_caption = 'audio_' + secrets.token_hex(5)
            telegram_file = requests.get(
                'https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, telegram_file_path))
            file_storage = FileSystemStorage()
            filename = 'users/' + file_caption
            extension = os.path.splitext(os.path.basename(telegram_file_path))[1]
            if os.path.exists(os.path.join(file_storage.location, filename + extension)):
                filename += secrets.token_hex(5)
            filename += extension
            filepath = os.path.join(file_storage.location, filename)
            open(filepath, 'wb').write(telegram_file.content)
            user = users.get_user_by_telegram_id(message.from_user.id)
            new_file = File.objects.create(name=file_caption,
                                           file_path=file_storage.path(filename),
                                           file_url=file_storage.url(filename),
                                           is_user_file=True,
                                           confirmed=False,
                                           caption='@send_sound_bot',
                                           user=user)
            type_filename_message = strings.get_string('user_files.type_file_name')
            remove_keyboard = keyboards.get_keyboard('remove')
            telegram_bot.send_message(message.chat.id, type_filename_message, reply_markup=remove_keyboard)
            telegram_bot.register_next_step_handler(message, file_name_handler, file_id=new_file.id)
        except Exception as e:
            error_message = strings.get_string('user_files.error')
            Navigation.to_main_menu(message.chat.id, error_message)
            logging.error(e)


def file_name_handler(message: Message, **kwargs):
    user_id = message.from_user.id
    file_id = kwargs.get('file_id')

    def error():
        error_message = strings.get_string('user_files.type_file_name')
        telegram_bot.reply_to(message, error_message)
        telegram_bot.register_next_step_handler_by_chat_id(user_id, file_name_handler, file_id=file_id)

    if not message.text:
        error()
        return
    file = files.get_file_by_id(file_id)
    file.rename_file(message.text)
    success_message = strings.get_string('user_files.success')
    Navigation.to_main_menu(user_id, success_message)
