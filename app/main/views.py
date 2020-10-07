# -*- coding: utf-8 -*-
from django import http
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from sitetree.sitetreeapp import get_sitetree

from .models import PageModel

UserModel = get_user_model()

__all__ = (
    'HomeView',
    'AboutView',
    'ContactView',
    'LoginView',
    'LogoutView',
)


class SiteTreeMixin:
    default_sitetree = "main"       # default

    @property
    def sitetree(self):
        return self.default_sitetree

    def current_sitetree(self, context):
        sitetree = get_sitetree()
        # noinspection PyUnresolvedReferences
        context['request'] = self.request
        sitetree.init_tree(self.sitetree, context)
        return sitetree.get_tree_current_item(self.sitetree)

    def get_pagemodel(self, context):
        item = self.current_sitetree(context)
        if item:
            try:
                return PageModel.objects.get(label__exact=item.url)
            except PageModel.DoesNotExist:
                pass
        return None


class TemplateSitetreeView(TemplateView, SiteTreeMixin):
    pass


class MarkdownPage(TemplateSitetreeView):
    template_name = 'main/markdownpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pagemodel'] = self.get_pagemodel(context)
        return context


class HomeView(MarkdownPage):
    pass


class AboutView(MarkdownPage):
    pass


class ContactView(MarkdownPage):
    commento = True


class UnderConstructionView(TemplateSitetreeView):
    template_name = 'main/under-construction.html'


class ArticlesView(UnderConstructionView):
    pass


class NewsView(UnderConstructionView):
    pass


class NewsView(UnderConstructionView):
    pass

class PrevPageMixin:
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


class LoginView(FormView, PrevPageMixin):
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


class LogoutView(View, PrevPageMixin):
    http_method_names = ['get']

    def get(self, request: http.HttpRequest, *args, **kwargs):
        self.set_success_url(request)
        logout(request)
        messages.warning(request, 'You have signed out.')
        return self.previous_page(request)
