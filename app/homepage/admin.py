from django.contrib import admin
from markdownx.admin import MarkdownxModelAdmin, AdminMarkdownxWidget
from markdownx.models import MarkdownxField

from .models import Page, InheritedPage

# Register your models here.


class PageAdmin(admin.ModelAdmin):
    readonly_fields = ('slug',)
    formfield_overrides = {
        MarkdownxField: {'widget': AdminMarkdownxWidget}
    }


class InheritedPageAdmin(PageAdmin):
    pass


admin.site.register(Page, PageAdmin)
admin.site.register(InheritedPage, InheritedPageAdmin)
