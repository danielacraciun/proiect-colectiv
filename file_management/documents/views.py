from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, DeleteView
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.timezone import now

from documents.models import Document
from documents.forms import DocumentForm
from documents.utils import check_integrity

# to do: add management commnd that deletes docs after 30 days

def workspace(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            existing_versioned = Document.objects.order_by('-version')
            existing = []
            origname = request.FILES['docfile'].name
            for item in existing_versioned:
                if origname.startswith(item.filename.split(".")[0]) and check_integrity(origname):
                    existing.append(item)
            newdoc = Document(docfile=request.FILES['docfile'], author=request.user, filename=request.FILES['docfile'].name)
            if existing:
                newdoc.filename = existing[0].filename
                newdoc.version = existing[0].get_next_version()
                for existing_doc in existing:
                    existing_doc.last_modified = newdoc.last_modified
                    existing_doc.stale = False
                    existing_doc.save()
            newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('workspace'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    # status 0 means draft
    documents = Document.objects.filter(status=0, author=request.user)
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
        return context


class CurrentTasks(TemplateView):
    #requiring action fluxes
    template_name = 'tasks.html'

    def get_context_data(self, **kwargs):
        context = super(CurrentTasks, self).get_context_data()
        return context


class FinishedTasks(TemplateView):
    # finished fluxes and docs
    template_name = 'fin_tasks.html'

    def get_context_data(self, **kwargs):
        context = super(FinishedTasks, self).get_context_data()
        return context


class DocumentDetailView(DetailView):
    model = Document
    template_name = 'document_detail.html'

    def get_queryset(self):
        current_user_docs = Document.objects.all()
        current_doc = current_user_docs.filter(pk=self.kwargs.get(self.pk_url_kwarg)).first()
        return current_user_docs.filter(filename=current_doc.filename)

    def get_context_data(self, **kwargs):
        context = super(DocumentDetailView, self).get_context_data(**kwargs)
        context['documents'] = self.get_queryset()
        context['doc_name'] = context['documents'].first().filename
        return context


class DocumentRemoveView(DeleteView):
    template_name = 'confirm.html'
    model = Document
    success_url = reverse_lazy('workspace')
    object = None

    def get_queryset(self):
        return Document.objects.filter(author=self.request.user)
