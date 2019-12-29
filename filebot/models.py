from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.core.files.storage import FileSystemStorage
from FileTelegramBot.settings import BASE_DIR
import os


class Category(MPTTModel):
    name = models.CharField(max_length=200)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    clicks = models.IntegerField(default=0)

    def add_click(self):
        self.clicks += 1
        self.save()

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
    name = models.CharField(max_length=200, blank=True, null=True)
    file_path = models.CharField(max_length=200)
    file_url = models.CharField(max_length=200, blank=True, null=True)
    is_user_file = models.BooleanField(default=False)
    hide_file_name = models.BooleanField(default=True)
    unprintable_file_name = models.BooleanField(default=False)
    show_full_name = models.BooleanField(default=False)
    confirmed = models.BooleanField(default=True)
    caption = models.TextField(max_length=500, blank=True, null=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey('BotUser', on_delete=models.CASCADE, blank=True, null=True, default=None)

    def get_full_file_name(self):
        return os.path.basename(self.file_path)

    def get_file_name(self):
        return os.path.splitext(self.get_full_file_name())[0]

    def get_file_extension(self):
        return os.path.splitext(self.get_full_file_name())[1]

    @property
    def file_name(self):
        return self.get_file_name()

    @property
    def full_file_name(self):
        return self.get_full_file_name()

    @property
    def extension(self):
        return self.get_file_extension()

    def remove_file(self):
        if os.path.exists(self.file_path):
            os.remove(self.file_path)

    def upload_file(self, file):
        self.remove_file()
        file_storage = FileSystemStorage()
        filename = file_storage.save(os.path.join(self.category.name, file.name), file)
        uploaded_file_url = os.path.join(BASE_DIR, file_storage.path(filename))
        self.file_path = uploaded_file_url
        self.file_url = file_storage.url(filename)
        self.save()

    def rename_file(self, new_name):
        file_storage = FileSystemStorage()
        extension = self.get_file_extension()
        file_category = self.category.name if self.category else 'users'
        new_file_name = os.path.join(file_category, new_name + extension)
        if file_storage.exists(os.path.join(file_category, new_name + extension)):
            return False
        old_file_name = self.file_name
        old_path = self.file_path
        new_path = os.path.join(file_storage.location, new_file_name)
        os.rename(old_path, new_path)
        self.file_path = new_path
        self.name = new_name
        self.file_url = file_storage.url(new_file_name)
        self.save()
        return old_file_name


class BotUser(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    username = models.CharField(max_length=200, null=True, blank=True)

    favorites_files = models.ManyToManyField(File)

    def favorite_file_exists(self, file: File):
        return file in self.favorites_files.all()


class Settings(models.Model):
    share_text = models.TextField(max_length=500, blank=True, null=True)
    share_photo = models.ImageField(upload_to='share/', blank=True, null=True)
    contacts_text = models.TextField(max_length=500, blank=True, null=True)
    start_message_text = models.TextField(max_length=500, blank=True, null=True)
