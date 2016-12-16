from django.core.management.base import BaseCommand, CommandError
from documents.models import Document
from datetime import datetime, timedelta
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Deletes stale documents that have been ready for deletion for more than 30 days'

    def handle(self, *args, **options):
        for doc in Document.objects.filter(stale=True):
            if now() - doc.stale_on >= timedelta(days=30):
                doc.delete()
