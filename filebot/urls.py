from django.urls import path
from .views import index, catalog, settings, bot
from FileTelegramBot.settings import WEBHOOK_URL_PATH

urlpatterns = [
    path('', index.IndexView.as_view(), name='admin-home'),
    path('catalog/', catalog.CategoryListView.as_view(), name='admin-catalog'),
    path('settings/', settings.SettingsView.as_view(), name='admin-settings'),
    path('catalog/<int:pk>', catalog.ShowCategoryChildrenView.as_view(), name='admin-catalog-categories-children'),
    path('catalog/<int:pk>/files', catalog.ShowCategoryFilesView.as_view(), name='admin-catalog-categories-files'),

    path('init/', bot.BotInitializeView.as_view()),
    path(WEBHOOK_URL_PATH, bot.BotUpdatesRecieverView.as_view())
]