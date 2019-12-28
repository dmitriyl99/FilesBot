from . import telegram_bot
from .utils import Access
from telebot.types import Message
from resources import strings
from filebot.models import File
from FileTelegramBot.settings import API_TOKEN
from django.core.files.storage import FileSystemStorage
import logging
import requests
import os
from core import users


@telegram_bot.message_handler(content_types=['text'], func=Access.upload)
def index_handler(message: Message):
    user_id = message.from_user.id
    helper_text = strings.get_string('user_files.help_text')
    telegram_bot.send_message(user_id, helper_text)


@telegram_bot.message_handler(content_types=['audio'])
def user_file_handler(message: Message):
    if message.photo:
        user_telegram_file = message.photo[-1]
    elif message.audio:
        user_telegram_file = message.audio
    elif message.document:
        user_telegram_file = message.document
    elif message.video:
        user_telegram_file = message.video
    else:
        return
    file_size_mb = user_telegram_file.file_size / 1024**2
    if file_size_mb > 1:
        too_much_size_message = strings.get_string('user_files.too_much_size')
        telegram_bot.reply_to(message, too_much_size_message)
    else:
        if not message.caption:
            caption_empty_message = strings.get_string('user_files.caption_empty')
            telegram_bot.reply_to(message, caption_empty_message)
            return
        try:
            wait_message = strings.get_string('user_files.wait')
            telegram_bot.reply_to(message, wait_message)
            telegram_file_info = telegram_bot.get_file(user_telegram_file.file_id)
            telegram_file_path = telegram_file_info.file_path
            file_caption = message.caption
            telegram_file = requests.get(
                'https://api.telegram.org/file/bot{0}/{1}'.format(API_TOKEN, telegram_file_path))
            file_storage = FileSystemStorage()
            filename = 'users/' + file_caption
            extension = os.path.splitext(os.path.basename(telegram_file_path))[1]
            filename += extension
            filepath = os.path.join(file_storage.location, filename)
            open(filepath, 'wb').write(telegram_file.content)
            user = users.get_user_by_telegram_id(message.from_user.id)
            File.objects.create(name=file_caption,
                                file_path=file_storage.path(filename),
                                file_url=file_storage.url(filename),
                                is_user_file=True,
                                caption='@send_sound_bot',
                                user=user)
            success_message = strings.get_string('user_files.success')
            telegram_bot.reply_to(message, success_message)
        except Exception as e:
            error_message = strings.get_string('user_files.error')
            telegram_bot.reply_to(message, error_message)
            logging.error(e)
