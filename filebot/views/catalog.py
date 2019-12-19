from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from filebot.models import Category
from filebot.forms import CategoryForm
from django.urls import reverse_lazy


class CategoryListView(LoginRequiredMixin, ListView):
    template_name = 'admin/catalog/categories/index.html'
    model = Category
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(level=0)


class ShowCategoryChildrenView(LoginRequiredMixin, ListView, SingleObjectMixin):
    template_name = 'admin/catalog/categories/show.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context

    def get_queryset(self):
        return self.object.get_children()


class ShowCategoryFilesView(LoginRequiredMixin, ListView, SingleObjectMixin):
    template_name = 'admin/catalog/categories/files.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context

    def get_queryset(self):
        return self.object.file_set.all()


class CreateCategoryView(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'parent']
    template_name = 'admin/catalog/categories/create.html'
    form_class = CategoryForm
    context_object_name = 'form'

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, "Категория %s добавлена!" % form.cleaned_data['name'])
        return result


class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['name', 'parent']
    template_name = 'admin/catalog/categories/edit.html'
    form_class = CategoryForm
    context_object_name = 'form'

    def form_valid(self, form):
        result = super().form_valid(form)
        messages.success(self.request, "Категория %s изменена!" % form.cleaned_data['name'])
        return result


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('admin_categories')

    def delete(self, request, *args, **kwargs):
        category_name = self.get_object().name
        result = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Категория %s удалена!" % category_name)
        return result
