from django.core.management.base import BaseCommand, CommandError
from documents.models import Document
from datetime import datetime, timedelta
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Marks documents older than 30 days as stale and ready for deletion'

    def handle(self, *args, **options):
        for doc in Document.objects.all():
            if now() - doc.last_modified >= timedelta(days=30):
                doc.stale=True
                doc.stale_on = now()
