from django.db import models

# Create your models here.


class TextContainer(models.Model):
    """
    A container for text paragraphs.
    """
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name or ''


class Paragraph(models.Model):
    """
    A simple paragraph of text.
    """
    text = models.TextField()
    container = models.ForeignKey(
        TextContainer, related_name='paragraphs', on_delete=models.CASCADE)

    def __str(self):
        return self.text or ''
