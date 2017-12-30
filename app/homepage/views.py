from django.shortcuts import redirect, reverse
from django.views import generic

from .models import TextPage, LinkedInAPITextPage


def root(request):
    return redirect(reverse('homepage:main-page', kwargs={'slug': 'main-page'}))


class TextPageView(generic.DetailView):
    model = TextPage


class LinkedInAPITextPageView(generic.DetailView):
    model = LinkedInAPITextPage
