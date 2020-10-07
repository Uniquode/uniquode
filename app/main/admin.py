from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin
from .models import PageModel


class PageModelAdmin(MarkdownxModelAdmin):
    list_display = ('label', 'dt_created', 'dt_modified')
    actions = None
    fieldsets = [
        (None, {
            'fields': [
                ('label', 'content')
            ]
        }),
    ]

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


admin.site.register(PageModel, PageModelAdmin)
