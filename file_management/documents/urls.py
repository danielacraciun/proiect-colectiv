from django.conf.urls import url
from django_downloadview import ObjectDownloadView
from documents import views, models

urlpatterns = [
    url(r'^workspace/$', views.workspace, name='workspace'),
    url(r'^init_tasks/$', views.InitiatedTasks.as_view(), name='init_tasks'),
    url(r'^current_tasks/$', views.CurrentTasks.as_view(), name='current_tasks'),
    url(r'^fin_tasks/$', views.FinishedTasks.as_view(), name='fin_tasks'),
    url(r'^new_task/$', views.NewTask.as_view(), name='new_task'),
    url(r'^new_task/(?P<pk>\d+)/', views.NewTask.as_view(), name='new_task_model'),
    url(r'^notifications/$', views.Notifications.as_view(), name='notifications'),
    url(r'^(?P<pk>\d+)/view', views.DocumentDetailView.as_view(), name='document_detail'),
    url(r'^(?P<pk>\d+)/remove', views.DocumentRemoveView.as_view(), name='remove_document'),
    url(r'^(?P<pk>\d+)/download', ObjectDownloadView.as_view(model=models.Document, file_field='docfile'), name='download'),
    url(r'^(?P<pk>\d+)/make_final', views.make_final, name='make_final'),
]
