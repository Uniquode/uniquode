from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from simple_history.models import HistoricalRecords
from simple_history import register
from markdownx.models import MarkdownxField


register(get_user_model(), app='main')


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Timestamps(models.Model):
    """
    Abstract model with auto-timestamps
    """
    dt_created = models.DateTimeField('Created', auto_now_add=True, editable=False)
    dt_modified = models.DateTimeField('Modified', auto_now=True, editable=False)

    class Meta:
        abstract = True


class PageModel(Timestamps):
    """
    Base document record
    """
    label = models.CharField('Label', max_length=64)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, # editable=False,
                                   on_delete=models.SET(get_sentinel_user),
                                   related_name='+', blank=True, null=True)
    content = MarkdownxField()
    history = HistoricalRecords()

    def __str__(self):
        return self.label
