from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.views.generic import FormView, RedirectView, TemplateView, UpdateView
from django.shortcuts import get_object_or_404, redirect

import logging

from user.forms import LoginForm
from user.models import UserProfile

class ProfileView(TemplateView):
    template_name = "user/profile.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data()
        user = get_object_or_404(User, pk=self.request.user.id)
        context['profile'] = user.profile
        return context

class HomeView(TemplateView):
    template_name = 'user/index.html'


class AuthLoginView(FormView):
    template_name = 'user/login.html'
    success_url = reverse_lazy('home')
    form_class = LoginForm

    def form_valid(self, form):
        logger = logging.getLogger('users')
        logger.info('User {} logged in'.format(form.fields['user']))
        login(self.request, form.fields['user'])
        return super(AuthLoginView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return redirect(reverse_lazy('home'))
        else:
            return self.render_to_response(self.get_context_data())


class AuthLogoutView(RedirectView):
    permanent = False
    query_string = True
    url = reverse_lazy('auth_login')

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            logger = logging.getLogger('users')
            logger.info('User {} logged out'.format(self.request.user))
            logout(self.request)
        return super(AuthLogoutView, self).get_redirect_url(*args, **kwargs)
