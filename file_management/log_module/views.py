from django.shortcuts import render
from django.core.urlresolvers import reverse
from log_module.models import Log
from log_module.forms import LogForm

# Create your views here.

def set_if_not_none(mapping, key, value):
    if value is not '':
        mapping[key] = value


def logs(request):
    if request.method == 'POST':
        form = LogForm(request.POST)
        if form.is_valid():
            filter_by = {}
            key_list = ['user', 'document', 'template', 'step', 'flow']
            for key in key_list:
                set_if_not_none(filter_by, key, form.cleaned_data[key])
            logs = Log.objects.filter(**filter_by)
    else:
        form = LogForm()
        logs = Log.objects.all()
    return render(
                request,
                'filter_logs.html',
                {'logs': logs, 'form': form}
            )


