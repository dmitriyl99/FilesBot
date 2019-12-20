from django.views.generic import DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from filebot.models import File
from FileTelegramBot.settings import BASE_DIR
from filebot.forms import FileForm
from django.urls import reverse_lazy, reverse
from django.core.files.storage import FileSystemStorage
import os


class CreateFileView(LoginRequiredMixin, FormView):
    template_name = 'admin/catalog/files/create.html'
    form_class = FileForm

    def get_success_url(self):
        return reverse('admin-catalog-categories-files', kwargs={'pk': self.category.id})

    def form_valid(self, form):
        category = form.cleaned_data['category']
        self.category = category
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


class UpdateFileView(LoginRequiredMixin, FormView, SingleObjectMixin):
    template_name = 'admin/catalog/files/edit.html'
    form_class = FileForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=File.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=File.objects.all())
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('admin-catalog-categories-files', kwargs={'pk': self.category.id})

    def form_valid(self, form):
        file = self.object
        category = form.cleaned_data['category']
        self.category = category
        file.category = category
        file.hide_file_name = form.cleaned_data['hide_file_name']
        file.show_full_name = form.cleaned_data['show_full_file_name']
        file.caption = form.cleaned_data['caption']
        file.save()
        uploadedFile = form.cleaned_data['file']
        if not uploadedFile and form.cleaned_data['name'] != file.file_name:
            result = file.rename_file(form.cleaned_data['name'])
            if result:
                messages.success(self.request, 'Имя файла было изменено c %s на %s'
                                 % (result, form.cleaned_data['name']))
            else:
                form.add_error('name', 'Файл с таким именем уже есть в категории %s' % category.name)
                return super().form_invalid(form)
        if uploadedFile:
            file.upload_file(uploadedFile)
        messages.success(self.request, 'Файл успешно отредактирован!')
        return super().form_valid(form)

