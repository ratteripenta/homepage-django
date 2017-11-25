from django.shortcuts import redirect, reverse, render_to_response
from django.template.response import TemplateResponse
from django.views import generic

from .models import NavigablePage, TextPage

# Create your views hereSlugReadOnlyWithMarkdownEditor.


def root(request):
    return render_to_response('base.html')


class TextPageView(generic.DetailView):
    model = TextPage
