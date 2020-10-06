# -*- coding: utf-8 -*-
from http import client as httpstatus

import pytest
from django.contrib.auth import get_user_model

from main import views as main_views

def standard_templates(logged_in=False):
    return (
        'layout.html',
        'base.html',
        'partials/_header.html',
        'partials/_logout.html' if logged_in else 'partials/_login.html',
        'partials/_navigation.html',
        'sitetree/menu.html',
        'sitetree/menu.html',
        'partials/_breadcrumbs.html',
        'sitetree/breadcrumbs.html',
        'partials/_footer.html',
    )

def template_viewtest(client, url, view, redirect=False, logged_in=False):
    if logged_in:
        user = get_user_model().objects.create(username='test', email='test@example.com')
        user.set_password('testtest')
        user.save()
        client.login(username='test', password='testtest')
    if redirect:
        response = client.get(url)
        assert response.status_code == httpstatus.MOVED_PERMANENTLY
        url += '/'
    response = client.get(url)
    assert response.status_code == httpstatus.OK
    assert view.template_name in response.template_name
    templates = [view.template_name] + [t for t in standard_templates(logged_in)]
    # expected set of templates rendered
    assert len(response.templates) == len(templates)
    for template in response.templates:
        assert template.name in templates


@pytest.mark.django_db
def test_homepage(client):
    template_viewtest(client, url='/', view=main_views.HomeView)


@pytest.mark.django_db
def test_homepage_user(client):
    template_viewtest(client, url='/', view=main_views.HomeView, logged_in=True)


@pytest.mark.django_db
def test_aboutpage(client):
    template_viewtest(client, url='/about', view=main_views.AboutView, redirect=True)


@pytest.mark.django_db
def test_aboutpage_user(client):
    template_viewtest(client, url='/about', view=main_views.AboutView, redirect=True, logged_in=True)


@pytest.mark.django_db
def test_contactpage(client):
    template_viewtest(client, url='/contact', view=main_views.ContactView, redirect=True)


@pytest.mark.django_db
def test_contactpage_user(client):
    template_viewtest(client, url='/contact', view=main_views.ContactView, redirect=True, logged_in=True)
