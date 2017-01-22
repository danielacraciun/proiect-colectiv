from django.core.urlresolvers import reverse, reverse_lazy
from django.forms import IntegerField, HiddenInput
from django.forms import ModelForm, ChoiceField, BaseForm, CharField
from django.http import Http404
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.html import format_html
from django.views.generic import CreateView
from django.views.generic import TemplateView, DetailView, DeleteView

from documents.forms import DocChoice, StepCreate
from documents.forms import DocumentForm
from documents.forms import FluxInstanceForm
from documents.models import Document, FluxInstance, FluxStatus, Step
from documents.models import FluxModel
from templateuri.models import Template
from user.models import Notification
from django.db.models import Q

import logging


def workspace(request):
    logger = logging.getLogger('documents')

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
            import pudb;pu.db
            newdoc = Document(docfile=request.FILES['docfile'], author=request.user,
                              filename=request.FILES['docfile'].name, abstract=request.POST['abstract'],
                              keywords=request.POST['keywords'],
                              requires_signature=request.POST['signature_required'] == 'on')
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
            elif existing and existing[0].status == 3:
                newdoc.filename = existing[0].filename
                for file in existing:
                    file.filename = "_" + file.filename
                newdoc.status = 0
                newdoc.version = 0.1
                newdoc.save()
            elif not existing:
                newdoc.version = 0.1
                newdoc.save()
            logger.info('User {} added version {} of Document {}'.format(request.user, newdoc.version, newdoc.filename))
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('workspace'))
    else:
        form = DocumentForm()  # A empty, unbound form

    # Load documents for the list page
    # status 0 means draft
    items = Document.objects.filter(status__in=[0, 1, 2], author=request.user).exclude(status=3)
    # Render list page with the documents and the form
    return render(
        request,
        'documents.html',
        {'documents': items, 'form': form}
    )


class FluxModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.s = kwargs.pop('steps', None)
        super(FluxModelForm, self).__init__(*args, **kwargs)
        self.fields['steps'].choices = self.s

    class Meta:
        model = FluxModel
        fields = ['title', 'steps', 'acceptance_criteria', 'groups', 'days_until_stale']
        widgets = {

        }
        success_url = reverse_lazy('workspace')


class CreateFlow(CreateView):
    form_class = FluxModelForm
    model = FluxModel
    template_name = 'create_flow.html'
    success_url = reverse_lazy('workspace')

    def get_form_kwargs(self):
        kwargs = super(CreateFlow, self).get_form_kwargs()
        kwargs['steps'] = Step.objects.filter(document=None).values_list('id', 'name')
        return kwargs


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
    logger = logging.getLogger('flows')
    # Handle file upload
    if request.method == 'POST':
        form = DocChoice(request.POST, request.FILES)
        new_doc_id = request.POST['doc_choice']
        step_id = request.POST['orig']
        s = Step.objects.get(id=step_id)
        s.document = Document.objects.get(id=new_doc_id)
        s.save()
        logger.info('User {} added Document {} for Step {}'.format(request.user, s.document.filename, s.name))
        return HttpResponseRedirect(reverse('flux_detail', kwargs={'pk': pk}))
    else:
        user_choices = list(Document.objects.filter(author=request.user, status__in=[1, 2]).values_list('id', 'filename', 'version'))
        user_choices = [(idx, filename + ": version %.2f" % version) for idx, filename, version in user_choices]
        fields = {'doc_choice': ChoiceField(choices=user_choices)}
        MyForm = type('DocChoice', (BaseForm,), {'base_fields': fields})
        form = MyForm()
    return render(
        request,
        'flux_detail.html',
        {'obj': FluxInstance.objects.filter(pk=pk).first(),
         'docs': Document.objects.filter(author=request.user),
         'form': form}
    )


def flux_manage_detail(request, pk):
    logger = logging.getLogger('flows')
    # Handle file upload
    if request.method == 'POST':
        form = DocChoice(request.POST, request.FILES)
        new_doc_id = request.POST.get('doc_choice')
        step_id = request.POST.get('orig')
        s = Step.objects.get(id=step_id) if step_id else None
        if s:
            s.document = Document.objects.get(id=new_doc_id) if new_doc_id else None
            s.save()
        return HttpResponseRedirect(reverse('flux_manage_detail', kwargs={'pk': pk}))
    else:
        user_choices = list(
            Document.objects.filter(author=request.user, status__in=[1, 2]).values_list('id', 'filename'))
        fields = {'doc_choice': ChoiceField(choices=user_choices)}
        MyForm = type('DocChoice', (BaseForm,), {'base_fields': fields})
        form = MyForm()
    return render(
        request,
        'flux_manage_detail.html',
        {'obj': FluxInstance.objects.filter(pk=pk).first(),
         'docs': Document.objects.filter(author=request.user),
         'form': form})


class CurrentTasks(TemplateView):
    # requiring action fluxes
    template_name = 'tasks.html'
    model = FluxInstance

    def get_queryset(self):
        id_list = []
        for parent in FluxModel.objects.all():
            if self.request.user in parent.acceptance_criteria.all():
                for instance in parent.instances.all():
                    if self.request.user not in instance.accepted_by.all() and instance.status != FluxStatus.REJECTED:
                        id_list.append(instance.id)
        return FluxInstance.objects.filter(id__in=id_list)

    def get_context_data(self, **kwargs):
        context = super(CurrentTasks, self).get_context_data()
        context['object_list'] = self.get_queryset()
        return context


class FinishedTasks(TemplateView):
    # finished fluxes and docs
    template_name = 'fin_tasks.html'
    model = FluxInstance

    def get_queryset(self):
        to_show_id = []
        tasks = FluxInstance.objects.filter(status__in=[FluxStatus.ACCEPTED, FluxStatus.REJECTED])
        for task in tasks:
            if task.initiated_by.id == self.request.user.id:
                to_show_id.append(task.id)
            elif self.request.user in task.flux_parent.acceptance_criteria.all():
                to_show_id.append(task.id)
        return FluxInstance.objects.filter(id__in=to_show_id)

    def get_context_data(self, **kwargs):
        context = super(FinishedTasks, self).get_context_data()
        context['object_list'] = self.get_queryset()
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
        logger = logging.getLogger('documents')
        logger.info('User {} removed version {} of Document {}'.format(self.request.user, model.version, model.filename))
        return Document.objects.filter(author=self.request.user)


def make_final(request, *args, **kwargs):
    logger = logging.getLogger('documents')
    obj = Document.objects.filter(id=kwargs['pk'])
    if not obj:
        logger.error('User {} encountered error. Could not find document'.format(request.user))
        raise Http404()
    obj = obj.first()
    obj.status = 1
    obj.version = obj.version + 1 if obj.version >= 1 else 1
    obj.save()
    logger.info('User {} made final Document {}'.format(request.user, obj.filename))
    return redirect('workspace')


def accept_flow(request, *args, **kwargs):
    logger = logging.getLogger('flows')
    obj = FluxInstance.objects.filter(id=kwargs['pk'])
    if not obj:
        logger.error('User {} encountered error. Could not find flux'.format(request.user))
        raise Http404()
    obj = obj.first()
    obj.accepted_by.add(request.user)
    obj.save()
    if set(obj.flux_parent.acceptance_criteria.all()).issubset(obj.accepted_by.all()):
        obj.status = 1
        obj.save()
        n = Notification(
            to_user=obj.initiated_by, flux=obj, from_user=request.user,
            message="Fluxul {} a fost acceptat de {}!".format(obj.flux_parent.title, request.user.username))
        n.save()
    logger.info('User {} accepted Flow {}'.format(request.user, obj.title))
    return redirect('current_tasks')


def reject_flow(request, *args, **kwargs):
    logger = logging.getLogger('flows')
    obj = FluxInstance.objects.filter(id=kwargs['pk'])
    if not obj:
        raise Http404()
    obj = obj.first()
    obj.status = 2
    obj.save()
    msg = request.POST.get('msg')
    if msg:
        n = Notification(
            to_user=obj.initiated_by, from_user=request.user, flux=obj,
            message="Fluxul {} a fost refuzat! Motiv: {}".format(obj.flux_parent.title, msg))
        n.save()
    logger.info('User {} rejected Flow {}'.format(request.user, obj.title))
    return redirect('current_tasks')


def step_create(request):
    logger = logging.getLogger('flows')
    # Handle file upload
    if request.method == 'POST':
        form = StepCreate(request.POST, request.FILES)
        title = request.POST['title']
        tmp_id = request.POST['template']
        t = Template.objects.get(id=tmp_id)
        s = Step(name=title, template_file=t, document=None)
        s.save()
        logger.info('User {} added Step {} with Template {}'.format(request.user, s.name, t.filename))
        return HttpResponseRedirect(reverse('create_flow'))
    else:
        user_choices = list(Template.objects.values_list('id', 'filename'))
        fields = {}
        fields['title'] = CharField(max_length=100)
        fields['template'] = ChoiceField(choices=user_choices)
        MyForm = type('StepCreate', (BaseForm,), {'base_fields': fields})
        form = MyForm()  # A empty, unbound form
    return render(
        request,
        'step_create.html',
        {'form': form}
    )


def review_flux(request, pk):
    # Handle file upload
    if request.method == 'POST':
        form = DocChoice(request.POST, request.FILES)
        new_doc_id = request.POST['doc_choice']
        step_id = request.POST['orig']
        s = Step.objects.get(id=step_id)
        s.document = Document.objects.get(id=new_doc_id)
        s.save()
        return HttpResponseRedirect(reverse('flux_manage_detail', kwargs={'pk': pk}))
    else:
        user_choices = list(
            Document.objects.filter(author=request.user, status__in=[1, 2]).values_list('id', 'filename'))
        fields = {'doc_choice': ChoiceField(choices=user_choices)}
        MyForm = type('DocChoice', (BaseForm,), {'base_fields': fields})
        form = MyForm()
    return render(
        request,
        'flux_view_detail.html',
        {'obj': FluxInstance.objects.filter(pk=pk).first(),
         'docs': Document.objects.filter(author=request.user),
         'form': form})


def new_flux(request, pk=None):
    if request.method == 'POST':
        obj = FluxInstance.objects.get(id=pk)
        for i, step in enumerate(obj.steps.all()):
            new_doc_id = request.POST['doc_choice_{}'.format(i)]
            step_id = request.POST['orig_id_{}'.format(i)]
            s = Step.objects.get(id=step_id)
            s.document = Document.objects.get(id=new_doc_id)
            s.save()

        for user in obj.flux_parent.acceptance_criteria.all():
            n = Notification(
                to_user=user, flux=obj, from_user=obj.initiated_by,
                message="Fluxul {} pornit de {} asteapta sa fie revizuit".format(obj.flux_parent.title, request.user.username))
            n.save()

        return HttpResponseRedirect(reverse_lazy('init_tasks'))
    else:
        flux_model = FluxModel.objects.filter(pk=request.GET['flux_model_select']).first()
        obj = FluxInstance(flux_parent=FluxModel.objects.filter(id=request.GET['flux_model_select']).first(),
                           initiated_by=request.user)
        obj.save()

        user_choices = list(
            Document.objects.filter(author=request.user, status__in=[1, 2]).values_list('id', 'filename'))
        fields = {"numsteps": IntegerField(widget=HiddenInput(), initial=len(list(flux_model.steps.all())))}

        links = {}

        for i, step in enumerate(flux_model.steps.all()):
            if (step.template_file):
                links.update({i: (step.name, step.template_file.id)})
            else :
                links.update({i: (step.name, None) })

            step.id = None
            step.save()
            obj.steps.add(Step.objects.latest('id'))
            fields.update({'doc_choice_{}'.format(i): ChoiceField(choices=user_choices, label=links[i])})
            fields.update({'orig_id_{}'.format(i): IntegerField(widget=HiddenInput(), initial=step.id)})

        MyForm = type('DocChoice', (BaseForm,), {'base_fields': fields})
        form = MyForm()

        print(request.GET['flux_model_select'])
        print(obj.flux_parent)

        return render(
            request,
            "new_task.html",
            {
                'obj': obj,
                'form': form,
                'links': links
            }
        )


def sign_doc(request, *args, **kwargs):
    logger = logging.getLogger('documents')
    obj = Document.objects.filter(id=kwargs['pk']).first()
    if not obj:
        logger.error('User {} encountered error. Could not find document'.format(request.user))
        raise Http404()
    obj.signed_by = request.user
    obj.signed = True
    obj.save()
    logger.info('User {} signed document {}'.format(request.user, obj.filename))
    return render(
        request,
        'flux_manage_detail.html',
        {'obj': FluxInstance.objects.filter(pk=kwargs['pkf']).first()})
