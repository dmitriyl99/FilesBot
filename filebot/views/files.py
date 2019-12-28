from django.views.generic import DeleteView, FormView, ListView, View
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from filebot.models import File
from FileTelegramBot.settings import BASE_DIR
from filebot.forms import FileForm
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
import os


class CreateFileView(LoginRequiredMixin, FormView):
    template_name = 'admin/catalog/files/create.html'
    form_class = FileForm

    def get_success_url(self):
        return reverse('admin-catalog-categories-files', kwargs={'pk': self.category.id})

    def form_valid(self, form):
        category = form.cleaned_data['category']
        self.category = category
        files = self.request.FILES.getlist('files')
        file_system = FileSystemStorage()
        for file in files:
            category_name = 'users' if form.cleaned_data['is_user_file'] else category.name
            filename = file_system.save(os.path.join(category_name, file.name), file)
            uploaded_file_url = os.path.join(BASE_DIR, file_system.path(filename))
            new_file = File.objects.create(file_path=uploaded_file_url,
                                           hide_file_name=not form.cleaned_data['hide_file_name'],
                                           unprintable_file_name=form.cleaned_data['unprintable_file_name'],
                                           caption='@send_sound_bot',
                                           is_user_file=form.cleaned_data['is_user_file'],
                                           file_url=file_system.url(filename),
                                           category=None if form.cleaned_data['is_user_file'] else category)
            new_file.name = new_file.get_file_name()
            new_file.save()
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
        if self.category:
            return reverse('admin-catalog-categories-files', kwargs={'pk': self.category.id})
        else:
            return reverse('admin-catalog-userfiles')

    def form_valid(self, form):
        file = self.object
        category = form.cleaned_data['category']
        self.category = category
        file.category = None if form.cleaned_data['is_user_file'] else category
        file.hide_file_name = not form.cleaned_data['hide_file_name']
        file.unprintable_file_name = form.cleaned_data['unprintable_file_name']
        file.caption = form.cleaned_data['caption']
        file.is_user_file = form.cleaned_data['is_user_file']
        file.save()
        uploaded_file = form.cleaned_data['files']
        if not uploaded_file and form.cleaned_data['name'] != file.file_name:
            result = file.rename_file(form.cleaned_data['name'])
            if result:
                messages.success(self.request, 'Имя файла было изменено c %s на %s'
                                 % (result, form.cleaned_data['name']))
            else:
                form.add_error('name', 'Файл с таким именем уже есть в категории %s' % category.name)
                return super().form_invalid(form)
        if uploaded_file:
            file.upload_file(uploaded_file)
        messages.success(self.request, 'Файл успешно отредактирован!')
        return super().form_valid(form)


class DeleteFileView(LoginRequiredMixin, DeleteView):
    model = File

    def get_success_url(self):
        return reverse('admin-catalog-categories-files', kwargs={'pk': self.category.id})

    def delete(self, request, *args, **kwargs):
        file = self.get_object()
        file_name = file.file_name
        self.category = file.category
        file.remove_file()
        result = super().delete(request, *args, **kwargs)
        messages.success(request, "Файл %s удалён" % file_name)
        return result


class UserFilesView(LoginRequiredMixin, ListView):
    model = File
    queryset = File.objects.filter(is_user_file=True).order_by('-id')
    template_name = 'admin/catalog/files/users.html'
    context_object_name = 'files'


class ConfirmUserFileView(LoginRequiredMixin, View, SingleObjectMixin):
    model = File

    def get(self, request, *args, **kwargs):
        file = self.get_object()
        file.confirmed = True
        file.save()
        messages.success(request, "Файл %s одобрен!" % file.name)
        return redirect('admin-catalog-userfiles')
