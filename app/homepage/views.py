from django.views import generic
from . import models
# Create your views here.


class PageView(generic.DetailView):
    model = models.Page
