from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, DeleteView
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.timezone import now


from templateuri.forms import TemplateForm
from templateuri.models import Template

import logging

def generate_filetype(filename):
    return "." + filename.split(".")[1]

def template_list(request):
    logger = logging.getLogger('templates')
    if request.method == 'POST':
        form = TemplateForm(request.POST, request.FILES)
        if form.is_valid():
            doc = request.FILES['docfile']
            origname = request.FILES['docfile'].name
            newdoc = Template(
                docfile=request.FILES['docfile'], filename=request.FILES['docfile'].name,
                filetype=generate_filetype(origname))
            newdoc.save()

            logger.info('User {} added Template {}'.format(request.user, newdoc.filename))
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('template_list'))
    else:
        form = TemplateForm()

    templates = Template.objects.all()
    items, item_ids = [], []
    for item in templates:
        if item.filename not in item_ids:
            items.append(item)
            item_ids.append(item.filename)

    return render(
        request,
        'templateuri.html',
        {'templates': items, 'form': form}
    )