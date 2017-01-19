from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import (
    password_reset, password_reset_done, password_reset_confirm, password_reset_complete)
from django.views.generic.base import RedirectView

from user.views import (
    HomeView, AuthLoginView, AuthLogoutView, ProfileView)


urlpatterns = [
    url(r'^home/$', RedirectView.as_view(pattern_name='workspace', permanent=False), name='home'),
    url(r'^profile/$', ProfileView.as_view(), name='user_profile'),
    url(r'^login/$', AuthLoginView.as_view(), name='auth_login'),
    url(r'^logout/$', AuthLogoutView.as_view(), name='auth_logout'),
    url(r'^password/reset/$', password_reset,
        {'post_reset_redirect': 'done/',
         'template_name': 'registration/password_reset_form_planner.html'},
        name="password_reset"),
    url(r'^password/reset/done/$', password_reset_done,
        {'template_name': 'registration/password_reset_done_planner.html'}),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z]+)/(?P<token>.+)/$', password_reset_confirm,
        {'post_reset_redirect': '/user/password/done/',
         'template_name': 'registration/password_reset_confirm_planner.html'},
        name='password_reset_confirm'),
    url(r'^password/done/$', password_reset_complete,
        {'template_name': 'registration/password_reset_complete_planner.html'},
        name='password_reset_done'),
    url(r'^change-password/$', auth_views.password_change,
        {'template_name': 'user/change-password.html'},
        name='change_password'),
    url(r'^change-password-done/$', auth_views.password_change_done,
        {'template_name': 'user/change-password-success.html'},
        name='password_change_done'),
]
