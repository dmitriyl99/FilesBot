from telebot import TeleBot
from FileTelegramBot import settings
from django.conf import settings


telegram_bot = TeleBot(settings.API_TOKEN)

if settings.DEBUG:
    import logging
    from telebot import logger
    logger.setLevel(logging.DEBUG)

from . import start, contacts, share, catalog, favorites, userfiles
