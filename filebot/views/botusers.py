from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from filebot.models import BotUser


class BotUsersIndexView(LoginRequiredMixin, ListView):
    template_name = 'admin/users/index.html'
    model = BotUser
    context_object_name = 'users'
