from django import forms

class LogForm(forms.Form):
    user = forms.CharField(max_length=100, label='Name of the user', required=False)
    document = forms.CharField(max_length=100, label='Name of the document', required=False)
    template = forms.CharField(max_length=100, label='Name of the template', required=False)
    step = forms.CharField(max_length=100, label='Name of the step', required=False)
    flow = forms.CharField(max_length=100, label='Name of the flow', required=False)
    date_from = forms.DateField(label='Logs starting from: ', required=False)
    date_to = forms.DateField(label='To: ', required=False)