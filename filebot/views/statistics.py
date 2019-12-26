from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from filebot.models import Category


class StatisticsIndexView(LoginRequiredMixin, ListView):
    template_name = 'admin/statistics/index.html'
    model = Category
    context_object_name = 'categories'
    ordering = ['-clicks']
