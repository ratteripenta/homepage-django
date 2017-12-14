from django import template

from homepage.models import NavigablePage, MarkdownText

register = template.Library()


@register.inclusion_tag('nav.html')
def navigation_pages(selected_id=None):
    return {
        'navigation_pages': NavigablePage.objects.all(),
        'selected_id': selected_id,
    }


@register.inclusion_tag('header.html')
def header(current_page=None):
    return {
        'header': MarkdownText.objects.get(target_section="header")
    }
