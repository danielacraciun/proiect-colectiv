from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    abstract = forms.CharField(max_length=100)
    keywords = forms.CharField(max_length=100, help_text='Separated by spaces.')