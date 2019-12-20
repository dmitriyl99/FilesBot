from django.views.generic import ListView
from django.views.generic.edit import DeleteView, FormView
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
    context_object_name = 'children'

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
    context_object_name = 'files'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object
        return context

    def get_queryset(self):
        return self.object.file_set.all()


class CreateCategoryView(LoginRequiredMixin, FormView):
    form_class = CategoryForm
    template_name = 'admin/catalog/categories/create.html'
    context_object_name = 'form'
    success_url = reverse_lazy('admin-catalog')

    def form_valid(self, form: CategoryForm):
        parent = form.cleaned_data['parent']
        category = Category.objects.create(name=form.cleaned_data['name'], parent=parent)
        result = super().form_valid(form)
        messages.success(self.request, "Категория %s добавлена!" % category.name)
        return result


class UpdateCategoryView(LoginRequiredMixin, FormView, SingleObjectMixin):
    template_name = 'admin/catalog/categories/edit.html'
    form_class = CategoryForm
    context_object_name = 'form'
    success_url = reverse_lazy('admin-catalog')

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Category.objects.all())
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        category = self.object
        parent = form.cleaned_data['parent']
        category.name = form.cleaned_data['name']
        category.move_to(parent)
        category.save()
        result = super().form_valid(form)
        messages.success(self.request, "Категория %s изменена!" % category.name)
        return result


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('admin-catalog')

    def delete(self, request, *args, **kwargs):
        category_name = self.get_object().name
        result = super().delete(request, *args, **kwargs)
        messages.success(self.request, "Категория %s удалена!" % category_name)
        return result
