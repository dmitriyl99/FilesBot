from django.views import View
from django.http import HttpRequest, HttpResponseBadRequest, HttpResponse
from telebot.types import Update
from FileTelegramBot.settings import WEBHOOK_URL_PATH, WEBHOOK_URL_BASE


class BotInitializeView(View):
    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        from bot import telegram_bot
        telegram_bot.remove_webhook()
        telegram_bot.set_webhook(WEBHOOK_URL_BASE + '/' + WEBHOOK_URL_PATH)
        return HttpResponse('Initialized Successfully!')


class BotUpdatesRecieverView(View):
    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if request.content_type != 'application/json':
            return HttpResponseBadRequest()
        json_string = request.body.decode('utf-8')
        update = Update.de_json(json_string)
        from bot import telegram_bot
        telegram_bot.process_new_updates([update])
        return HttpResponse('')
