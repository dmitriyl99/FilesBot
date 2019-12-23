from . import telegram_bot
from .utils import Access
from telebot.types import Message
from core import settings
from resources import strings


@telegram_bot.message_handler(content_types=['text'], func=Access.share)
def share_handler(message: Message):
    chat_id = message.chat.id

    bot_settings = settings.get_settings()
    if bot_settings and bot_settings.share_text:
        if bot_settings.share_photo:
            telegram_bot.send_photo(chat_id, open(bot_settings.share_photo.path, 'rb'),
                                    caption=bot_settings.share_text, parse_mode='HTML')
        else:
            telegram_bot.send_message(chat_id, bot_settings.share_text, parse_mode='HTML')
    else:
        telegram_bot.send_message(chat_id, strings.get_string('share.no_share_text'))
