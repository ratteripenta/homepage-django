import os
import sys
from homepage.models import MarkdownText, TextPage

HOMEPAGE_MD_FOLDER = os.path.join(
    os.getcwd(), 'homepage', 'initializations', 'markdown')


def create_models():
    """
    Create default models.
    """

    for md in os.listdir(HOMEPAGE_MD_FOLDER):
        md_path = os.path.join(HOMEPAGE_MD_FOLDER, md)

    content = ""
    with open(md_path, 'r') as f:
        content = "".join(f.readlines())

    title = md.replace("-", " ").split(".")[0]

    if title == 'header':

        model, created = MarkdownText.objects.create_or_update(
            target_section='header',
            content=content
        )
        print(model, "created={}".format(created))

    else:

        if title == 'main page':
            order = 1
        elif title == 'about me':
            order = 2
        else:
            order = 3

        model, created = TextPage.objects.create_or_update(
            order=order,
            title=title.title(),
            content=content
        )
        print(model, "created={}".format(created))


if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
    create_models()
