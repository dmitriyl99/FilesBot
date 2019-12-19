from django import forms
from mptt.forms import TreeNodeChoiceField
from filebot.models import Category, File


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=200)
    parent = TreeNodeChoiceField(queryset=Category.objects.all())


class FilesForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['hide_file_name', 'show_full_name', 'caption', 'category']
