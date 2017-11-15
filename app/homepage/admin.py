from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin, AdminMarkdownxWidget
from markdownx.models import MarkdownxField

from .models import Page

# Register your models here.


class PageAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget}
    }


admin.site.register(Page, PageAdmin)
