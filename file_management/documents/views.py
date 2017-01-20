from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, DeleteView
from documents.forms import DocumentForm
from documents.models import Document


# to do: add management commnd that deletes docs after 30 days
from user.models import Notification


def workspace(request):
    # Handle file upload
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            existing_versioned = Document.objects.order_by('-version')
            origname = request.FILES['docfile'].name
            existing = []
            for item in existing_versioned:
                if item.filename and origname.startswith(item.filename.split(".")[0]):
                    existing.append(item)
            newdoc = Document(docfile=request.FILES['docfile'], author=request.user,
                              filename=request.FILES['docfile'].name)
            if existing and existing[0].status == 0:
                newdoc.filename = existing[0].filename
                newdoc.version = existing[0].version + 0.1
                for existing_doc in existing:
                    existing_doc.last_modified = newdoc.last_modified
                    existing_doc.stale = False
                    existing_doc.save()
                newdoc.save()
            elif existing and existing[0].status == 1:
                newdoc.filename = existing[0].filename
                if existing[0].author == request.user:
                    newdoc.status = 1
                    newdoc.version = existing[0].version + 1
                else:
                    newdoc.status = 2
                    newdoc.version = existing[0].version + 0.1
                newdoc.save()
            elif existing and existing[0].status == 2:
                newdoc.filename = existing[0].filename
                newdoc.status = 2
                newdoc.version = existing[0].version + 0.1
                newdoc.save()
            elif not existing:
                newdoc = Document(docfile=request.FILES['docfile'], author=request.user,
                                  filename=request.FILES['docfile'].name)
                newdoc.version = 0.1
                newdoc.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('workspace'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    # status 0 means draft
    documents = Document.objects.filter(status__in=[0, 1, 2], author=request.user)
    items, item_ids = [], []
    for item in documents:
        if item.filename not in item_ids:
            items.append(item)
            item_ids.append(item.filename)
    blocked = Document.objects.filter(status=3, author=request.user)
    items = [x for x in items if x.filename not in map(lambda x: x.filename, blocked)]
    # Render list page with the documents and the form
    return render(
        request,
        'documents.html',
        {'documents': items, 'form': form}
    )


class CreateFlow(TemplateView):
    template_name = 'create_flow.html'

    def get_context_data(self, **kwargs):
        context = super(CreateFlow, self).get_context_data()
        context['create_flow'] = Notification.objects.filter(to_user=self.request.user)
        return context


class Notifications(TemplateView):
    template_name = 'notifications.html'

    def get_context_data(self, **kwargs):
        context = super(Notifications, self).get_context_data()
        context['notifications'] = Notification.objects.filter(to_user=self.request.user)
        return context


class InitiatedTasks(TemplateView):
    # all fluxes
    template_name = 'init_tasks.html'

    def get_context_data(self, **kwargs):
        context = super(InitiatedTasks, self).get_context_data()
        return context


class CurrentTasks(TemplateView):
    # requiring action fluxes
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


def make_final(request, *args, **kwargs):
    obj = Document.objects.filter(id=kwargs['pk'])
    if not obj:
        raise Http404()
    obj = obj.first()
    obj.status = 1
    obj.save()
    obj.version += 1
    obj.save()
    return redirect('workspace')
