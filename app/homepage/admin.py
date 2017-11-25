from django.contrib import admin
from markdownx.admin import AdminMarkdownxWidget, MarkdownxModelAdmin
from markdownx.models import MarkdownxField

from . import models


class SlugReadOnly(admin.ModelAdmin):
    readonly_fields = ('slug',)


class SlugReadOnlyWithMarkdownEditor(SlugReadOnly):
    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget}
    }


admin.site.register(models.NavigablePage, SlugReadOnly)
admin.site.register(models.TextPage, SlugReadOnlyWithMarkdownEditor)
