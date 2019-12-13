from . import telegram_bot
from .utils import Access
from core import settings
from telebot.types import Message
from resources import strings


@telegram_bot.message_handler(content_types=['text'], func=Access.contacts)
def contacts_handler(message: Message):
    chat_id = message.chat.id

    bot_settings = settings.get_settings()
    if bot_settings and bot_settings.contacts_text:
        telegram_bot.send_message(chat_id, bot_settings.contacts_text, parse_mode='HTML')
    else:
        telegram_bot.send_message(chat_id, strings.get_string('contacts.no_contacts'))
