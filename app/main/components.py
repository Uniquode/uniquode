# -*- coding: utf-8 -*-
"""
Some useful model building blocks
"""
import uuid

from django.db import models
from django.db.models import UUIDField


class TimestampModel(models.Model):
    """
    Abstract model with auto-timestamps
    """
    dt_created = models.DateTimeField('Created', auto_now_add=True, editable=False)
    dt_modified = models.DateTimeField('Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    id = UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class ActivatedModel(models.Model):
    is_active = models.BooleanField(default=False)

    def activate(self, save=True):
        if self.is_active:
            raise ValueError(f'{self.__class__.__name__} Already activated')
        self.is_active = True
        if save:
            self.save()

    class Meta:
        abstract = True
