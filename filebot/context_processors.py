from bot import telegram_bot


def telegram_bot_info_processor(request):
    return {'bot_info': telegram_bot.get_me()}
