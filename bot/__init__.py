from telebot import TeleBot
from django.conf import settings
import logging
from telebot import logger


telegram_bot = TeleBot(settings.API_TOKEN)

if settings.DEBUG:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.ERROR)

from . import start, contacts, share, catalog, favorites, userfiles, search

from .utils import Access, Navigation


@telegram_bot.message_handler(content_types=['text'], func=Access.empty)
def empty_handler(message):
    Navigation.to_main_menu(message.chat.id)
