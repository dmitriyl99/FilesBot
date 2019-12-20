from django.views.generic import DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from filebot.models import File
from FileTelegramBot.settings import BASE_DIR
from filebot.forms import FileForm
from django.urls import reverse_lazy
from django.core.files.storage import FileSystemStorage
import os


class CreateFileView(LoginRequiredMixin, FormView):
    template_name = 'admin/catalog/files/create.html'
    form_class = FileForm
    success_url = reverse_lazy('admin-catalog')

    def form_valid(self, form):
        category = form.cleaned_data['category']
        file = form.cleaned_data['file']
        file_system = FileSystemStorage()
        filename = file_system.save(os.path.join(category.name, file.name), file)
        uploaded_file_url = os.path.join(BASE_DIR, file_system.path(filename))
        new_file = File.objects.create(file_path=uploaded_file_url,
                                       hide_file_name=form.cleaned_data['hide_file_name'],
                                       show_full_name=form.cleaned_data['show_full_file_name'],
                                       caption=form.cleaned_data['caption'],
                                       category=category)
        messages.success(self.request,
                         "Файл %s добавлен в категорию %s" % (new_file.get_full_file_name(), category.name))
        result = super().form_valid(form)
        return result
