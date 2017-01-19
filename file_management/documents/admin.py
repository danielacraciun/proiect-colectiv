from django.contrib import admin
from documents.models import Document
from documents.models import Step
from documents.models import FluxModel
from documents.models import FluxInstance

admin.site.register(Document)
admin.site.register(Step)
admin.site.register(FluxModel)
admin.site.register(FluxInstance)
