from django.conf.urls import url
from log_module import views, models

urlpatterns = [
    url(r'^filter_logs/$', views.logs, name='filter_logs'),
    ]