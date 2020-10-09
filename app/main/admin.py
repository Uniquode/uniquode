from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.utils.timesince import timesince
from markdownx.admin import MarkdownxModelAdmin

from .models import Page, Message, Article


class CreatedByMixin:

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class PageAdmin(CreatedByMixin, MarkdownxModelAdmin):
    list_display = ('label', 'dt_created', 'dt_modified')
    actions = None
    fieldsets = [
        (None, {
            'fields': [
                ('label', 'content')
            ]
        }),
    ]


admin.site.register(Page, PageAdmin)


class MessagesAdmin(CreatedByMixin, ModelAdmin):
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

    # noinspection PyMethodMayBeStatic
    def since_created(self, obj):
        return timesince(obj.dt_created)


admin.site.register(Message, MessagesAdmin)


class ArticlesAdmin(CreatedByMixin, ModelAdmin):
    pass


admin.site.register(Article, ArticlesAdmin)
