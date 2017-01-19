from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

urlpatterns = [
    url(r'^$', RedirectView.as_view(url='/usr/login')),
    url(r'^admin/', admin.site.urls),
    url(r'^usr/', include('user.urls')),
    url(r'^documents/', include('documents.urls'), name='workspace'),
    url(r'^templates/', include('templateuri.urls')),
]
