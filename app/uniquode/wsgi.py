"""
WSGI config for uniquode project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from utils import env
from django.core.wsgi import get_wsgi_application

env.load()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniquode.settings')

application = get_wsgi_application()
