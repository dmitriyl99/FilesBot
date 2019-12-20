from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
import os


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    @property
    def has_children(self):
        return self.get_children().count() > 0

    @property
    def children(self):
        return self.get_children()

    @property
    def has_files(self):
        return self.file_set.count() > 0

    @property
    def ancestors(self):
        return self.get_ancestors()

    def __str__(self):
        return self.name


class File(models.Model):
    file_path = models.CharField(max_length=200)
    is_user_file = models.BooleanField(default=False)
    hide_file_name = models.BooleanField(default=False)
    show_full_name = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)
    caption = models.TextField(max_length=500, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_full_file_name(self):
        return os.path.basename(self.file_path)

    def get_file_name(self):
        return os.path.splitext(self.get_full_file_name())[0]

    def get_file_extension(self):
        return os.path.splitext(self.get_full_file_name())[1]


class BotUser(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)

    favorites_files = models.ManyToManyField(File)

    def favorite_file_exists(self, file: File):
        return file in self.favorites_files.all()


class Settings(models.Model):
    share_text = models.TextField(max_length=500, blank=True, null=True)
    contacts_text = models.TextField(max_length=500, blank=True, null=True)
    start_message_text = models.TextField(max_length=500, blank=True, null=True)
