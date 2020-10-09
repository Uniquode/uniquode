# -*- coding: utf-8 -*-
from django import http
from django.contrib import messages
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView, FormView
from sitetree.sitetreeapp import get_sitetree

from .models import Page
from .forms import MessageForm


UserModel = get_user_model()

__all__ = (
    'HomeView',
    'AboutView',
    'MessagesView',
    'LoginView',
    'LogoutView',
)


class PrevPageMixin:
    """
    Mixin for handing back to the calling page via modal form
    """
    success_url = reverse_lazy('home')

    def get_success_url(self):
        return self.success_url

    def set_success_url(self, request: http.HttpRequest, usenext: bool = True):
        if usenext:
            try:
                self.success_url = request.GET['next']
                return
            except KeyError:
                pass
        self.success_url = request.META.get('HTTP_REFERER', self.success_url)

    def previous_page(self, request):
        return HttpResponseRedirect(self.success_url)


class SiteTreeMixin:
    """
    Tie markdown page content to page sitetree.item
    """
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

    def get_page(self, context):
        item = self.current_sitetree(context)
        if item:
            try:
                return Page.objects.get(label__exact=item.url)
            except Page.DoesNotExist:
                pass
        return None


class TemplateSitetreeView(TemplateView, SiteTreeMixin):
    pass


class MarkdownPage(TemplateSitetreeView):
    template_name = 'main/markdownpage.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = self.get_page(context)
        return context


class HomeView(MarkdownPage):
    pass


class AboutView(MarkdownPage):
    pass


class MessagesView(FormView, MarkdownPage, PrevPageMixin):
    """
    Requires the following html in the page to pop out the contact form:
    <button type="button" class="primary" title="Contact Form" aria-label="Contact Form">
      <label for="modal-control-contact"><i class="fas fa-user"></i></label>
    </button>
    """
    template_name = 'main/markdownpage-contact.html'
    form_class = MessageForm
    commento = True

    def post(self, request: http.HttpRequest, *args, **kwargs):
        self.set_success_url(request)
        # type: MessageForm
        form = self.get_form()
        if form.is_valid():
            # noinspection PyUnresolvedReferences
            form.instance.created_by = request.user
            if form.save():
                messages.info(self.request, 'Message sent')
                return self.form_valid(form)
        # post messages for all errors
        for field, error in form._errors.items():
            messages.error(self.request, f'{field}: {error}')
        return self.form_invalid(form)


class UnderConstructionView(TemplateSitetreeView):
    template_name = 'main/under-construction.html'


class ArticlesView(UnderConstructionView):
    pass


class NewsView(UnderConstructionView):
    pass


class TestView(LoginRequiredMixin, MarkdownPage):
    pass


class LoginView(FormView, PrevPageMixin):
    http_method_names = ['post', 'put']
    # use form class from django.contrib.auth to handle the authorisation
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
