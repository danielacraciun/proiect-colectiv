from django.conf.urls import url
from django.views.generic import RedirectView

from documents import views

urlpatterns = [
    url(r'^workspace/$', views.workspace, name='workspace'),
    url(r'^init_tasks/$', views.InitiatedTasks.as_view(), name='init_tasks'),
    url(r'^current_tasks/$', views.CurrentTasks.as_view(), name='current_tasks'),
    url(r'^fin_tasks/$', views.FinishedTasks.as_view(), name='fin_tasks'),
    # url(r'^(?P<pk>\d+)/edit', views.UserEditRequest.as_view(), name='edit_request'),
]
