from django import template

from homepage.models import Page

register = template.Library()


@register.inclusion_tag('nav.html')
def navigation_pages(selected_id=None):
    return {
        'navigation_pages': Page.objects.all(),
        'selected_id': selected_id,
    }
