from django.views.generic import UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import FileSystemStorage
from filebot.models import Settings
from django.urls import reverse_lazy
from django.contrib import messages
from filebot.forms import AdvertisingPostForm
from bot.utils import Helpers
import os


class SettingsView(LoginRequiredMixin, UpdateView):
    template_name = 'admin/settings/index.html'
    model = Settings
    fields = ['share_text', 'contacts_text', 'start_message_text', 'share_photo']
    success_url = reverse_lazy('admin-settings')

    def get_object(self, queryset=None):
        return Settings.objects.first()

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, 'Настройки сохранены!')
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['advertising_form'] = AdvertisingPostForm()
        return context


class AdvertisingPostView(LoginRequiredMixin, FormView):
    form_class = AdvertisingPostForm
    success_url = reverse_lazy('admin-settings')

    def form_valid(self, form):
        text = form.cleaned_data['text']
        file = form.cleaned_data['file']
        file_path = None
        if file:
            file_storage = FileSystemStorage()
            filename = file_storage.save(os.path.join('advertising', file.name), file)
            file_path = file_storage.path(filename)
        Helpers.distribute_advertising_post(text, file_path)
        if file:
            file_storage.delete(filename)
        messages.success(self.request, "Рассылка прошла успешно!")
