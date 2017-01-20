from django import forms

from documents.models import Document


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    abstract = forms.CharField(max_length=100)
    keywords = forms.CharField(max_length=100, help_text='Separated by spaces.')

class DocChoice(forms.Form):
    doc_choice = forms.ChoiceField(choices=Document.objects.values_list('id', 'filename'))
    orig_id = forms.IntegerField()