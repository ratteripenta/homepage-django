from django.contrib import admin
from markdownx.admin import AdminMarkdownxWidget, MarkdownxModelAdmin
from markdownx.models import MarkdownxField

from . import models


class SlugReadOnly(admin.ModelAdmin):
    readonly_fields = ('slug',)


class MarkdownEditor(admin.ModelAdmin):
    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget}
    }


class SlugReadOnlyWithMarkdownEditor(SlugReadOnly, MarkdownEditor):
    pass


admin.site.register(models.NavigablePage, SlugReadOnly)
admin.site.register(models.TextPage, SlugReadOnlyWithMarkdownEditor)
admin.site.register(models.MarkdownText, MarkdownEditor)
admin.site.register(models.LinkedInAPIClient)

admin.site.site_header = "Homepage of Petteri Nevavuori"
