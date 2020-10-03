# -*- encoding: utf-8 -*-
from pathlib import Path
import cbs
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
APP_DIR = Path(__file__).resolve().parent
BASE_DIR = APP_DIR.parent
TOP_DIR = BASE_DIR.parent

APP_NAME = 'uniquode'


class Env:
    def __init__(self):
        import os
        self._env = os.environ

    def get(self, var, default=None):
        return self._env.get(var, default)

    def set(self, var, value=None):
        if value is None:
            if self.get(var) is not None:
                del self._env[var]
        else:
            self._env[var] = value

    def int(self, var, default=None):
        val = self.get(var, default)
        return int(val) if val is not None and val.isdigit() else None

    def bool(self, var, default=None):
        val = self.get(var, default)
        return True if val and any([val.startswith(v) for v in ('T', 't', '1', 'on', 'Y', 'y', 'ena')]) else False


env = Env()
MODE = env.get('DJANGO_MODE', 'dev').title()

# although they will be overwridden these allow pycharm to resolve {% static %}
STATICFILES_DIRS = [  # where static files are found
    BASE_DIR / 'static',
]
STATICFILES_FINDERS = [
    'npm.finders.NpmFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]


class BaseSettings:
    SECRET_KEY = env.get('DJANGO_SECRET_KEY')
    DEBUG = env.bool('DJANGO_DEBUG', default=False)
    ALLOWED_HOSTS = []

    # Application definition
    INSTALLED_APPS = [
        'main',

        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'django.middleware.cache.FetchFromCacheMiddleware',     # must be last
    ]

    ROOT_URLCONF = f'{APP_NAME}.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [
                BASE_DIR / 'templates'
            ],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

    WSGI_APPLICATION = f'{APP_NAME}.wsgi.application'
    ASGI_APPLICATION = f'{APP_NAME}.asgi:application'

    # Database
    DATABASES = {
        'default': dj_database_url.config('DJANGO_DATABASE_URL', conn_max_age=1800)
    }

    # Redis cache: Pages and session cache
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': env.get('DJANGO_REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient'
            }
        },
        'sessions': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': env.get('DJANGO_REDIS_URL'),
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient'
            }
        }
    }
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
    SESSION_CACHE_ALIAS = 'sessions'

    MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

    # Password validation
    AUTH_PASSWORD_VALIDATORS = [
        {
            'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
        },
        {
            'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
        },
    ]

    # Internationalization
    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [                    # where static files are found
        BASE_DIR / 'static',
    ]
    STATICFILES_FINDERS = [
        'npm.finders.NpmFinder',
        'django.contrib.staticfiles.finders.FileSystemFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ]
    STATIC_ROOT = TOP_DIR / 'static'        # where static files are collected
    NPM_ROOT_PATH = BASE_DIR
    NPM_FILE_PATTERNS = {
        'mini.css': ['']
    }

class DevSettings(BaseSettings):
    pass


class TestSettings(DevSettings):
    pass


class BetaSettings(BaseSettings):
    pass


class ProdSettings(BetaSettings):
    pass


cbs.apply(f'{MODE}Settings', globals())