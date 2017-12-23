from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class NavigablePage(models.Model):
    """
    A base model for each page with an associated link in the navigation bar.
    """
    class Meta:
        ordering = ('order',)

    order = models.PositiveIntegerField(unique=True)
    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title or ''


class TextPage(NavigablePage):
    """
    A model for a single page with Markdown content.
    """

    content = MarkdownxField()

    @property
    def content_md(self):
        return markdownify(self.content)


class MarkdownText(models.Model):
    """
    A model for injectable static Markdown text.
    """

    target_section = models.CharField(max_length=20)
    content = MarkdownxField()

    @property
    def content_md(self):
        return markdownify(self.content)

    def __str__(self):
        return self.target_section or ''


class LinkedInAPIClient(models.Model):
    """
    A model for containing required information or LinkedIn OAuth2 cycle.

    Docs: https://developer.linkedin.com/docs/oauth2
    """
    client_id = models.CharField(max_length=64, unique=True)
    client_secret = models.CharField(max_length=64, unique=True)
    redirect_uri = models.URLField()
    state = models.CharField(max_length=64)
    authorization_code = models.CharField(max_length=1024)
    access_token = models.CharField(max_length=1024)
    expires_in = models.PositiveIntegerField()

    def __str__(self):
        return self.client_id or ''
