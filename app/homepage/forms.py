from django import forms
from . import models


class PageContentForm(forms.ModelForm):

    class Meta:
        model = models.Page
        fields = ['content']
