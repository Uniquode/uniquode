# -*- coding: utf-8 -*-
from http import client as httpstatus
from main import views as main_views

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == httpstatus.OK
    assert main_views.HomeView.template_name in response.template_name
    # expected set of templates rendered
    templates = (
        main_views.HomeView.template_name,
        'base.html',
        'layout.html',
        'partials/_header.html',
        'partials/_navigation.html',
        'partials/_footer.html',
    )
    assert len(response.templates) == len(templates)
    for template in response.templates:
        assert template.name in templates


def test_aboutpage(client):
    response = client.get('/about')
    assert response.status_code == httpstatus.MOVED_PERMANENTLY
    response = client.get('/about/')
    assert response.status_code == httpstatus.OK
    assert main_views.AboutView.template_name in response.template_name
    # expected set of templates rendered
    templates = (
        main_views.AboutView.template_name,
        'base.html',
        'layout.html',
        'partials/_header.html',
        'partials/_navigation.html',
        'partials/_footer.html',
    )
    assert len(response.templates) == len(templates)
    for template in response.templates:
        assert template.name in templates
