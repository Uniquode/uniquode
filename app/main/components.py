# -*- coding: utf-8 -*-
"""
Some useful model building blocks
"""
import uuid

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import UUIDField

__all__ = (
    'TimestampModel',
    'AuthorModel',
    'UUIDModel',
    'ActivatedModel',
    'get_user_model',
    'get_sentinel_user'
)


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class TimestampModel(models.Model):
    """
    Abstract model with auto-timestamps
    """
    dt_created = models.DateTimeField('Created', auto_now_add=True, editable=False)
    dt_modified = models.DateTimeField('Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class AuthorModel(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, editable=False,
                                   on_delete=models.SET(get_sentinel_user),
                                   related_name='+', blank=True, null=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class ActivatedModel(models.Model):
    is_active = models.BooleanField(default=False)

    def activate(self, state=True, save=True):
        if self.is_active == state:
            raise ValueError(f'{self.__class__.__name__} Already {"activated" if state else "inactivated"}')
        self.is_active = state
        if save:
            self.save()

    def deactivate(self, state=False, save=True):
        self.activate(state, save)

    class Meta:
        abstract = True
