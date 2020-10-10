from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.html import format_html
from django.utils.timesince import timesince
from markdownx.admin import MarkdownxModelAdmin

from .models import Page, Message, Article, Icon


class CreatedByMixin:

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class TimestampMixin:

    # noinspection PyMethodMayBeStatic
    def since_created(self, obj):
        return timesince(obj.dt_created)

    # noinspection PyMethodMayBeStatic
    def since_modified(self, obj):
        return timesince(obj.dt_created)


class TaggedMixin:

    # noinspection PyUnresolvedReferences
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def _tags(self, obj):
        return ", ".join(o.name for o in obj.tags.all())


class PageAdmin(CreatedByMixin, TimestampMixin, MarkdownxModelAdmin):
    list_display = ('label', 'since_created', 'since_modified')
    actions = None
    fieldsets = [
        (None, {
            'fields': [
                ('label', 'content')
            ]
        }),
    ]


admin.site.register(Page, PageAdmin)


class MessagesAdmin(CreatedByMixin, TimestampMixin, ModelAdmin):
    list_display = ('id', 'since_created', 'created_by', 'message_name', 'message_email', 'topic')
    actions = None
    fieldsets = [
        (None, {
            'fields': [
                ('to', 'name', 'email', 'topic', 'text')
            ]
        }),
    ]

    def message_name(self, obj):
        return f'{obj.created_by.first_name} {obj.created_by.last_name}' if obj.created_by else obj.name

    def message_email(self, obj):
        return f'{obj.created_by.email}' if obj.created_by else obj.email


admin.site.register(Message, MessagesAdmin)


class IconAdmin(ModelAdmin, TaggedMixin):
    list_display = ('_svg', 'name', '_tags')

    def _svg(self, obj):
        return format_html(obj.svg)

    class Meta:
        ordering = ['name']


admin.site.register(Icon, IconAdmin)


class ArticlesAdmin(CreatedByMixin, ModelAdmin):
    pass


admin.site.register(Article, ArticlesAdmin)
