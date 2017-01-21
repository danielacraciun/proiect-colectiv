from django.core.urlresolvers import reverse, reverse_lazy
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.shortcuts import render

from documents.forms import DocumentForm, DocChoice

from django.views.generic import CreateView
from django.views.generic import TemplateView, DetailView, DeleteView
from documents.forms import DocumentForm, FluxInstanceForm
from documents.models import Document, FluxInstance, FluxStatus, Step

# to do: add management commnd that deletes docs after 30 days
from user.models import Notification

from documents.models import FluxModel


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


class CreateFlow(CreateView):
    template_name = 'create_flow.html'
    # form_class = FluxModelForm
    model = FluxModel
    fields = ['title', 'steps', 'acceptance_criteria', 'groups', 'days_until_stale']
    success_url = reverse_lazy('workspace')

    # def get_context_data(self, **kwargs):
    #     context = super(CreateFlow, self).get_context_data()
    #     context['create_flow'] = Notification.objects.filter(to_user=self.request.user)
    #     return context


class Notifications(TemplateView):
    template_name = 'notifications.html'

    def get_context_data(self, **kwargs):
        context = super(Notifications, self).get_context_data()
        context['notifications'] = Notification.objects.filter(to_user=self.request.user)
        return context


class InitiatedTasks(TemplateView):
    # all fluxes
    template_name = 'init_tasks.html'
    model = FluxInstance

    def get_queryset(self):
        tasks = FluxInstance.objects.filter(initiated_by=self.request.user).filter(status=FluxStatus.PENDING)
        return tasks

    def get_context_data(self, **kwargs):
        context = super(InitiatedTasks, self).get_context_data()
        context['object_list'] = self.get_queryset()
        context['form'] = FluxInstanceForm
        return context


def flux_detail(request, pk):
    # Handle file upload
    if request.method == 'POST':
        form = DocChoice(request.POST, request.FILES)
        new_doc_id = request.POST['doc_choice']
        step_id = request.POST['orig']
        s = Step.objects.get(id=step_id)
        s.document = Document.objects.get(id=new_doc_id)
        s.save()
        return HttpResponseRedirect(reverse('flux_detail', kwargs={'pk': pk}))
    else:
        form = DocChoice()  # A empty, unbound form
    return render(
        request,
        'flux_detail.html',
        {'obj': FluxInstance.objects.filter(pk=pk).first(),
         'docs': Document.objects.filter(author=request.user),
         'form': form}
    )


class CurrentTasks(TemplateView):
    # requiring action fluxes
    template_name = 'tasks.html'

    def get_queryset(self):
        tasks = FluxInstance.objects.filter(flux_parent__acceptance_criteria=self.request.user).exclude(
            accepted_by=self.request.user).distinct();
        return tasks

    def get_context_data(self, **kwargs):
        context = super(CurrentTasks, self).get_context_data(**kwargs)
        context['fluxes'] = self.get_queryset()
        return context


class FinishedTasks(TemplateView):
    # finished fluxes and docs
    template_name = 'fin_tasks.html'

    def get_queryset(self):
        tasks = FluxInstance.objects.filter(initiated_by=self.request.user).exclude(status=FluxStatus.PENDING);
        return tasks

    def get_context_data(self, **kwargs):
        context = super(FinishedTasks, self).get_context_data()
        context['fluxes'] = self.get_queryset()
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
    obj.version = obj.version + 1 if obj.version >= 1 else 1
    obj.save()
    return redirect('workspace')


def new_flux(request, pk=None):
    if pk:
        obj = FluxInstance.objects.get(id=pk)
    if request.method == 'POST':
        form = DocChoice(request.POST, request.FILES)
        new_doc_id = request.POST['doc_choice']
        step_id = request.POST['orig']
        s = Step.objects.get(id=step_id)
        s.document = Document.objects.get(id=new_doc_id)
        s.save()

        # if finish:
        return HttpResponseRedirect(reverse_lazy('init_tasks'))
        # return HttpResponseRedirect(reverse('new_flux', kwargs={'obj': obj}))
    else:
        form = DocChoice()
        flux_model = FluxModel.objects.filter(pk=request.GET['flux_model_select']).first()
        obj = FluxInstance(flux_parent=FluxModel.objects.filter(id=request.GET['flux_model_select']).first(),
                           initiated_by=request.user)
        obj.save()
        print(request.GET['flux_model_select'])
        print(obj.flux_parent)
        for step in flux_model.steps.all():
            step.id = None
            step.save()
            obj.steps.add(Step.objects.latest('id'))

    return render(
        request,
        "new_task.html",
        {
            'obj': obj,
            'form': form
        }
    )
