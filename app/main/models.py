from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager
import simple_history
import simple_history.models as history_models

# noinspection PyUnresolvedReferences
from .components import (
    TimestampModel,
    AuthorModel,
    UUIDModel,
    ActivatedModel,
    get_sentinel_user
)


simple_history.register(get_user_model(), app='main')


class Page(TimestampModel, AuthorModel):
    """
    Base document record
    """
    label = models.CharField(_('Label'), max_length=64, db_index=True)
    content = MarkdownxField(_('Content'))
    history = history_models.HistoricalRecords(_('History'))

    def __str__(self):
        return self.label


class Message(UUIDModel, TimestampModel, AuthorModel):
    to = models.ForeignKey(settings.AUTH_USER_MODEL,
                           on_delete=models.SET_NULL,
                           related_name='+', blank=True, null=True)
    name = models.CharField(_('Name'), max_length=64, blank=True, null=True)
    email = models.EmailField(_('Email'), max_length=64, blank=True, null=True)
    topic = models.CharField(_('Topic'), max_length=255, blank=False)
    text = models.TextField(_('Message'))

    def __str__(self):
        bits = [
            f'Id:{self.id}',
            f'From<{self.name}>',
        ]
        if self.to:
            bits.append(f'To<{self.to}>')
        bits.append(f'Re<{self.topic}>')
        return ' '.join(bits)


class Icon(models.Model):
    name = models.CharField(_('Icon Name'), primary_key=True, max_length=64, blank=False, null=False)
    svg = models.TextField(_('SVG'))


class Category(models.Model):
    name = models.CharField(_('Category Name'), max_length=64, blank=False, null=False)
    svg = models.ForeignKey(Icon, to_field='name', on_delete=models.SET_NULL, related_name='+', null=True)
    history = history_models.HistoricalRecords(_('History'))


class Article(UUIDModel, TimestampModel, AuthorModel, ActivatedModel):
    title = models.CharField(_('Title'), max_length=255)
    slug = models.SlugField(_('Slug'), max_length=64)
    tags = TaggableManager(_('Tags'))
    page = models.OneToOneField(Page, on_delete=models.CASCADE, related_name='articles')
    history = history_models.HistoricalRecords(_('History'))

    def __str__(self):
        return f'{self.title} {self.dt_created} ({self.slug})'
