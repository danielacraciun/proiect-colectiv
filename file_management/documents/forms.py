from django import forms

from documents.models import FluxModel


class DocumentForm(forms.Form):
    docfile = forms.FileField(label='Select a file')
    abstract = forms.CharField(max_length=100)
    keywords = forms.CharField(max_length=100, help_text='Separated by spaces.')
    signature_required = forms.BooleanField()

    def is_valid(self):
        return True


class DocChoice(forms.Form):
    doc_choice = forms.ChoiceField(choices=[])
    orig_id = forms.IntegerField()


class FluxInstanceForm(forms.Form):
    flux_model_select = forms.ModelChoiceField(queryset=FluxModel.objects.order_by('title').all())


class FluxCompletionForm(forms.Form):
    numsteps = forms.IntegerField()


class StepCreate(forms.Form):
    title = forms.CharField(max_length=100)
    tmps = forms.ChoiceField(choices=[])
