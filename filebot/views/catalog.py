from django.views.generic import ListView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from filebot.models import Category


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
