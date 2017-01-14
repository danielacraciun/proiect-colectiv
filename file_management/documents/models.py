# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
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


class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d/')
    filename = models.CharField(max_length=100, null=True, blank=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='documents', null=True, blank=True)
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
