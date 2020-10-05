"""
ASGI config for uniquode project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os
from utils import env
from django.core.asgi import get_asgi_application

env.load()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uniquode.settings')

application = get_asgi_application()
