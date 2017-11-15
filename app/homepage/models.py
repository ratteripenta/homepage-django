from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify

# Create your models here.


class Page(models.Model):
    """
    A model for a single page with Markdown content.
    """

    class Meta:
        ordering = ('title',)

    slug = models.SlugField(unique=True, null=True)
    title = models.CharField(max_length=100, unique=True)
    content = MarkdownxField()

    @property
    def content_md(self):
        return markdownify(self.content)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or ''
