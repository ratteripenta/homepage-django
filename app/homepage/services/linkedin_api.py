from urllib.parse import urlencode, urlparse

from django.conf import settings
from django.shortcuts import redirect, reverse, render_to_response
from homepage.models import LinkedInAPIClient


def request_authorization_code(request):

    api_client = LinkedInAPIClient.objects.first()

    if not api_client:
        return "No LinkedInAPIClients in DB!"

    params = {
        'response_type': 'code',
        'client_id': api_client.client_id,
        'redirect_uri': api_client.redirect_uri,
        'state': api_client.state,
    }

    url = "{}?{}".format(settings.LINKEDIN_AUTH_URL, urlencode(params))
    print("linkedin_api.request_authorization_code: url={}".format(url))

    return redirect(url)


def exchange_code_to_token(request):
    return request
