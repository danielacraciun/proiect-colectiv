from django.shortcuts import render
from django.views.generic import TemplateView
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from documents.models import Document
from documents.forms import DocumentForm

# to do: add management commnd that deletes docs after 30 days

def workspace(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            existing = Document.objects.filter(filename=request.FILES['docfile'].name).order_by('-version').first()
            newdoc = Document(docfile=request.FILES['docfile'], author=request.user, filename=request.FILES['docfile'].name)
            if existing:
                newdoc.version = existing.get_next_version()
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('workspace'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    #todo: keep only docs that are not in fluxes
    documents = Document.objects.all()
    items, item_ids = [], []
    for item in documents:
        if item.filename not in item_ids:
            items.append(item)
            item_ids.append(item.filename)

    # Render list page with the documents and the form
    return render(
        request,
        'documents.html',
        {'documents': items, 'form': form}
    )

class InitiatedTasks(TemplateView):
    # all fluxes
    template_name = 'init_tasks.html'

    def get_context_data(self, **kwargs):
        context = super(InitiatedTasks, self).get_context_data()
        context['hello'] = 'bello'
        return context


class CurrentTasks(TemplateView):
    #requiring action fluxes
    template_name = 'tasks.html'

    def get_context_data(self, **kwargs):
        context = super(CurrentTasks, self).get_context_data()
        context['hello'] = 'bello'
        return context


class FinishedTasks(TemplateView):
    # finished fluxes and docs
    template_name = 'fin_tasks.html'

    def get_context_data(self, **kwargs):
        context = super(FinishedTasks, self).get_context_data()
        context['hello'] = 'bello'
        return context
