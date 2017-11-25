from django import template

from homepage.models import NavigablePage

register = template.Library()


@register.inclusion_tag('nav.html')
def navigation_pages(selected_id=None):
    return {
        'navigation_pages': NavigablePage.objects.all(),
        'selected_id': selected_id,
    }
