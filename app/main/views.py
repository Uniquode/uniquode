# -*- coding: utf-8 -*-
from django.views.generic import TemplateView

__all__ = (
    'HomeView',
    'AboutView',
)


class HomeView(TemplateView):
    template_name = 'main/index.html'


class AboutView(TemplateView):
    template_name = 'main/about.html'
