import os
import uuid

from django.conf import settings
from django.db import models
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify


class NavigablePage(models.Model):
    """
    A base model for each page with an associated link in the navigation bar.
    """
    class Meta:
        verbose_name = "Navigable Page"
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
    class Meta:
        verbose_name = "Text Page"

    content = MarkdownxField()

    @property
    def content_md(self):
        return markdownify(self.content)


class LinkedInAPITextPage(TextPage):
    """
    A model for page with content partially retrieved from LinkedIn REST API.
    """
    class Meta:
        verbose_name = 'LinkedIn API Text Page'

    profile_id = models.CharField(max_length=80, unique=True, null=True)
    headline = models.CharField(max_length=256, null=True)
    industry = models.CharField(max_length=256, null=True)
    summary = models.CharField(max_length=2048, null=True)
    current_job_description = models.CharField(max_length=1024, null=True)
    profile_url = models.URLField(null=True)

    def save(self, *args, **kwargs):
        self.content = "".join(open(os.path.join(
            settings.HOMEPAGE_MD_FOLDER, 'career-bio.md')).readlines()),

        text = "\n The information has been retrieved directly from my [personal LinkedIn page]({}), where you can easily find out more about my current and past studies and positions.\n\n".format(
            self.profile_url)

        text += "##### CURRENT TITLE\n\n"
        #text += "---\n"
        text += "> {}\n\n".format(self.headline)

        text += "##### CURRENT JOB DESCRIPTION\n\n"
        #text += "---\n"
        text += "> {}\n\n".format(self.current_job_description)

        text += "##### INDUSTRY\n\n"
        #text += "---\n"
        text += "> {}\n\n".format(self.industry)

        text += "##### BRIEF SUMMARY\n\n"
        #text += "---\n"
        text += "> {}\n\n".format(self.summary)

        self.content = "".join(self.content + (text,))

        super().save(*args, **kwargs)


class MarkdownText(models.Model):
    """
    A model for injectable static Markdown text.
    """
    class Meta:
        verbose_name = "Markdown Text"

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
    class Meta:
        verbose_name = "LinkedIn API Client"

    linkedin_app = models.CharField(max_length=64,
                                    verbose_name="LinkedIn App")
    api_call_url = models.URLField(verbose_name="LinkedIn API Auth URL",
                                   null=True)
    client_id = models.CharField(max_length=64,
                                 unique=True,
                                 verbose_name='Client ID')
    client_secret = models.CharField(max_length=64,
                                     unique=True,
                                     verbose_name='Client Secret')
    redirect_uri = models.URLField(verbose_name="Redirect URI",
                                   null=True)
    state = models.UUIDField(default=uuid.uuid4,
                             editable=False)
    access_token = models.CharField(max_length=1024,
                                    editable=False,
                                    null=True)
    expires_in = models.PositiveIntegerField(editable=False,
                                             null=True)

    def __str__(self):
        return self.linkedin_app or ''
