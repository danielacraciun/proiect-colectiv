from django import forms
from django.contrib.auth.models import User, Group

from templateuri.models import Template


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    abstract = forms.CharField(max_length=100)
    keywords = forms.CharField(max_length=100, help_text='Separated by spaces.')


class StepForm(forms.Form):
    name = forms.CharField(max_length=100)
    template_file = forms.ModelMultipleChoiceField(queryset=Template.objects.all())


class FluxModelForm(forms.Form):
    title = forms.CharField(max_length=100)
    steps = forms.ModelMultipleChoiceField(queryset=Template.objects.all())
    acceptance_criteria = forms.ModelMultipleChoiceField(queryset=User.objects.all())
    groups = forms.ModelMultipleChoiceField(queryset=Group.objects.all())
    days_until_stale = forms.IntegerField()
