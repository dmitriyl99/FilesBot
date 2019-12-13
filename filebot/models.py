from django.db import models
from treebeard.mp_tree import MP_Node
import os


class Category(MP_Node):
    name = models.CharField(max_length=200)


class File(models.Model):
    file_path = models.CharField(max_length=200)
    is_user_file = models.BooleanField(default=False)
    hide_file_name = models.BooleanField(default=False)
    show_full_name = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=False)

    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def get_full_file_name(self):
        return os.path.basename(self.file_path)

    def get_file_name(self):
        return os.path.splitext(self.get_full_file_name())[0]


class BotUser(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)

    favorites_files = models.ManyToManyField(File)


class Settings(models.Model):
    share_text = models.TextField(max_length=500, blank=True, null=True)
    contacts_text = models.TextField(max_length=500, blank=True, null=True)
    start_message_text = models.TextField(max_length=500, blank=True, null=True)
