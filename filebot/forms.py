from django import forms
from mptt.forms import TreeNodeChoiceField
from filebot.models import Category, File


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=200)
    parent = TreeNodeChoiceField(queryset=Category.objects.all(), required=False)


class FileForm(forms.Form):
    name = forms.CharField(max_length=200, required=False)
    caption = forms.CharField(max_length=500, required=False)
    files = forms.FileField(allow_empty_file=True, required=False)
    hide_file_name = forms.BooleanField(required=False)
    show_full_file_name = forms.BooleanField(required=False)
    unprintable_file_name = forms.BooleanField(required=False)
    is_user_file = forms.BooleanField(required=False)
    category = TreeNodeChoiceField(queryset=Category.objects.all(), required=False)


class AdvertisingPostForm(forms.Form):
    text = forms.CharField(max_length=5000)
    file = forms.FileField(required=False)
