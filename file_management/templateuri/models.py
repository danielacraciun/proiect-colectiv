from django.db import models
from django.utils.timezone import now


# Create your models here.


class Template(models.Model):
    docfile = models.FileField(upload_to='templateuri/%Y/%m/%d/')
    filename = models.CharField(max_length=100, null=True, blank=True)
    created_on = models.DateTimeField(blank=False, default=now)
    fields = models.CharField(max_length=2500, null=False, blank=False)
    filetype = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return '{}'.format(self.filename)

    def file_link(self):
        if self.docfile:
            return "<a download href='%s'>download</a>" % (self.docfile.url,)
        else:
            return "No attachment"
