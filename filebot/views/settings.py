from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from filebot.models import Settings


class SettingsView(LoginRequiredMixin, DetailView):
    template_name = 'admin/settings/index.html'
    context_object_name = 'settings'

    def get_object(self, queryset=None):
        return Settings.objects.first()
