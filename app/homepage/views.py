from django.shortcuts import redirect, reverse, render_to_response
from django.template.response import TemplateResponse
from django.views import generic

from .models import NavigablePage, TextPage, LinkedInAPIClient


def root(request):
    return redirect(reverse('homepage:main-page', kwargs={'slug': 'main-page'}))


class TextPageView(generic.DetailView):
    model = TextPage
