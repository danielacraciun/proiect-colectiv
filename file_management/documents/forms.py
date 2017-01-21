from django import forms
from django.contrib.auth.models import User, Group
from django.db import OperationalError

from documents.models import Document
from templateuri.models import Template


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    abstract = forms.CharField(max_length=100)
    keywords = forms.CharField(max_length=100, help_text='Separated by spaces.')


class DocChoice(forms.Form):
    try:
        doc_choice = forms.ChoiceField(choices=Document.objects.values_list('id', 'filename'))
    except OperationalError:
        doc_choice = forms.ChoiceField(choices=[])
    orig_id = forms.IntegerField()