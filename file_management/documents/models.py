# -*- coding: utf-8 -*-
from datetime import datetime

from django.contrib.auth.models import User, Group
from django.db import models
from django.utils.timezone import now

"""
DRAFT – prima versiune de document de tip draft va fi 0.1. Draft-urile urmatoare vor primi
versiuni incrementate cu 0.1 (ex. 0.2, 0.3, ....., 0.12). Documentele de tip draft nu pot putea fi
incluse in fluxuri de documente, pot exista doar in zona de lucru a utilizatorului;
- FINAL – proprietarul documentului poate schimba statusul documentului din draft in final.
Prima versiune finala a documentului va fi versiunea 1.0. Modificari ale versiunii 1.0 vor primi
numere de versiuni incrementate cu 1.0 (ex. 2.0, 3.0, 4.0 ..... 12.0)
- FINAL REVIZUIT – reviziile / modificarile facute de persoanele care nu sunt proprietarii/
titularul documentului vor putea revizui sau modifica documentul doar daca au acest drept
iar versiunile vor fi incrementate pornind de la versiunea X.1, unde X este ultima versiune
finala lansata in flux de catre utilizatorul titular al documentului. In momentul primei revizuiri
/ modificari ale documentului statusul lui se schimba automat din final in final revizuit.
- BLOCAT – toate documentele vor primi automat statusul blocat in momentul cand fluxul de
documente din care face parte a fost finalizat. Documentele cu acest status se vor gasi doar
in zona task -urilor terminate
"""


class DocumentState:
    DRAFT = 0
    FINAL = 1
    REVISED_FINAL = 2
    BLOCKED = 3
    CHOICES = (
        (DRAFT, "Draft"),
        (FINAL, "Final"),
        (REVISED_FINAL, "Final revizuit"),
        (BLOCKED, "Blocat")
    )


class FluxStatus:
    PENDING = 0
    ACCEPTED = 1
    REJECTED = 2
    CHOICES = (
        (PENDING, "Pending"),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected")
    )


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d/')
    filename = models.CharField(max_length=100, null=True, blank=True)
    author = models.ForeignKey(User, related_name='documents', null=True, blank=True)
    created_on = models.DateTimeField(blank=False, default=now)
    last_modified = models.DateTimeField(blank=False, default=now)
    abstract = models.CharField(max_length=100, null=True, blank=True)
    keywords = models.CharField(max_length=100, null=True, blank=True)
    status = models.IntegerField(
        choices=DocumentState.CHOICES, default=DocumentState.DRAFT)
    version = models.FloatField(null=False, blank=False, default=0.1)
    signed = models.BooleanField(null=False, blank=False, default=False)
    stale = models.BooleanField(null=False, blank=False, default=False)
    stale_on = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return '{}'.format(self.filename)

    def get_next_version(self):
        if self.status == DocumentState.DRAFT or DocumentState.REVISED_FINAL:
            return self.version + 0.1
        elif self.status == DocumentState.FINAL:
            return self.version + 1
        return self.version

    def file_link(self):
        if self.docfile:
            return "<a download href='%s'>download</a>" % (self.docfile.url,)
        else:
            return "No attachment"

    def sign_doc(self):
        if self.status == DocumentState.FINAL or DocumentState.REVISED_FINAL:
            self.signed = True
        else:
            raise Exception

    file_link.allow_tags = True


class Step(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, default="step_name")
    template_file = models.ForeignKey(Document, related_name='template_step_fluxes', null=True, blank=True)
    document = models.ForeignKey(Document, related_name='document_step_fluxes', null=True, blank=True, default=None)

    def is_template_instance(self):
        return self.template_file is None or self.template_file.strip() == ""

    def get_template_link(self):
        if self.template_file.docfile:
            return "<a download href='%s'>%s</a>" % (self.template_file.docfile, self.name,)
        return "No attachment"

    def get_document_link(self):
        if self.template_file.docfile:
            return "<a download href='%s'>%s</a>" % (self.document.docfile, self.document.filename,)
        return "No attachment"

    def __str__(self):
        return '{}'.format(self.name, )


class FluxModel(models.Model):
    title = models.CharField(max_length=100, null=False, blank=False, default="flux_name")
    steps = models.ManyToManyField(Step, related_name='in_model_fluxes', blank=False)
    acceptance_criteria = models.ManyToManyField(User, related_name='flux_models', blank=True)
    groups = models.ManyToManyField(Group, related_name='visible_flux')
    days_until_stale = models.IntegerField(null=False, blank=False, default=30)

    def __str__(self):
        return '{}'.format(self.title, )


class FluxInstance(models.Model):
    flux_parent = models.ForeignKey(FluxModel, on_delete=models.CASCADE, related_name='instances', null=False,
                                    blank=False)
    steps = models.ManyToManyField(Step, related_name='in_instance_fluxes', blank=True, default=None)
    accepted_by = models.ManyToManyField(User, related_name='accepted_flux', blank=True, default=None)
    created_on = models.DateTimeField(null=False, blank=False, default=now)
    initiated_by = models.ForeignKey(User, blank=False, null=False)
    status = models.IntegerField(choices=FluxStatus.CHOICES, default=FluxStatus.PENDING)

    def is_accepted(self):
        return set(self.accepted_by.all()).issubset(set(self.flux_parent.acceptance_criteria.all()))

    def until_stale(self):
        return (datetime.now() - self.created_on).days

    def is_stale(self):
        return self.until_stale() <= 0

    def __str__(self):
        return '{} parent: {}'.format(self.id, self.flux_parent.title, )
