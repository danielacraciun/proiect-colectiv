from django.db import models

# Create your models here.
class Log(models.Model):
    created = models.TextField(db_column='Created', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    loglevel = models.IntegerField(db_column='LogLevel', blank=True, null=True)  # Field name made lowercase.
    loglevelname = models.TextField(db_column='LogLevelName', blank=True, null=True)  # Field name made lowercase.
    message = models.TextField(db_column='Message', blank=True, null=True)  # Field name made lowercase.
    args = models.TextField(db_column='Args', blank=True, null=True)  # Field name made lowercase.
    module = models.TextField(db_column='Module', blank=True, null=True)  # Field name made lowercase.
    funcname = models.TextField(db_column='FuncName', blank=True, null=True)  # Field name made lowercase.
    lineno = models.IntegerField(db_column='LineNo', blank=True, null=True)  # Field name made lowercase.
    exception = models.TextField(db_column='Exception', blank=True, null=True)  # Field name made lowercase.
    process = models.IntegerField(db_column='Process', blank=True, null=True)  # Field name made lowercase.
    thread = models.TextField(db_column='Thread', blank=True, null=True)  # Field name made lowercase.
    threadname = models.TextField(db_column='ThreadName', blank=True, null=True)  # Field name made lowercase.
    user = models.TextField(db_column='User', blank=True, null=True)  # Field name made lowercase.
    document = models.TextField(db_column='Document', blank=True, null=True)  # Field name made lowercase.
    template = models.TextField(db_column='Template', blank=True, null=True)  # Field name made lowercase.
    step = models.TextField(db_column='Step', blank=True, null=True)  # Field name made lowercase.
    flow = models.TextField(db_column='Flow', blank=True, null=True)  # Field name made lowercase.