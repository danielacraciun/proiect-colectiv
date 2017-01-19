from django.conf.urls import url
from django.views.generic import RedirectView
from django_downloadview import ObjectDownloadView

from templateuri import views, models

urlpatterns = [
    url(r'^template_list/$', views.template_list, name='template_list'),
    url(r'^(?P<pk>\d+)/download', ObjectDownloadView.as_view(
        model=models.Template, file_field='docfile'), name='download_template'),
    ]