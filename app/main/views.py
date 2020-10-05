# -*- coding: utf-8 -*-
from django import http
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView


UserModel = get_user_model()

__all__ = (
    'HomeView',
    'AboutView',
    'ContactView',
    'LoginView',
    'LogoutView',
)


class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)


class AboutView(TemplateView):
    template_name = 'main/about.html'


class ContactView(TemplateView):
    template_name = 'main/contact.html'


class PrevPageView:
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url

    def set_success_url(self, request: http.HttpRequest):
        try:
            self.success_url = request.GET['next']
        except KeyError:
            self.success_url = request.META.get('HTTP_REFERER', self.success_url)

    def previous_page(self, request):
        return HttpResponseRedirect(self.success_url)


class LoginView(FormView, PrevPageView):
    http_method_names = ['post', 'put']
    form_class = AuthenticationForm

    def post(self, request: http.HttpRequest, *args, **kwargs):
        self.set_success_url(request)
        form = self.get_form()
        if form.is_valid():
            login(request, form.get_user())
            messages.info(request, 'You have signed in.')
            return self.form_valid(form)
        messages.error(request, 'Authentication failed.')
        return self.previous_page(request)


class LogoutView(View, PrevPageView):
    http_method_names = ['get']

    def get(self, request: http.HttpRequest, *args, **kwargs):
        self.set_success_url(request)
        logout(request)
        messages.warning(request, 'You have signed out.')
        return self.previous_page(request)
