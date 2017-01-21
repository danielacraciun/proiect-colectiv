from django import forms
from documents.models import FluxModel


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    abstract = forms.CharField(max_length=100)
    keywords = forms.CharField(max_length=100, help_text='Separated by spaces.')


class FluxModelSelectionForm(forms.Form):
    flux_parent = forms.ModelChoiceField(queryset=FluxModel.objects.all().order_by('title'))
