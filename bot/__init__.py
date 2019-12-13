from telebot import TeleBot
from FileTelegramBot import settings


telegram_bot = TeleBot(settings.API_TOKEN)

from . import start, contacts, share
