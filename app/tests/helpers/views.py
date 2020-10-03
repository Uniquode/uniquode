# -*- coding: utf-8 -*-

def setup_view(view, request, *args, **kwargs):
    """
    Mimic ``as_view()``, but returns view instance.
    Use this function to get view instances on which you can run unit tests,
    by testing specific methods.
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view
