from django.views.generic import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from filebot.models import Settings
from django.urls import reverse_lazy
from django.contrib import messages


class SettingsView(LoginRequiredMixin, UpdateView):
    template_name = 'admin/settings/index.html'
    model = Settings
    fields = ['share_text', 'contacts_text', 'start_message_text']
    success_url = reverse_lazy('admin-settings')

    def get_object(self, queryset=None):
        return Settings.objects.first()

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'Настройки сохранены!')
        return result
