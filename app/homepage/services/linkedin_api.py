from urllib.parse import urlencode, urlparse

import requests
from django.conf import settings
from django.shortcuts import redirect, reverse

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
    return redirect(url)


def exchange_code_to_token(request):

    api_client = LinkedInAPIClient.objects.first()

    if not api_client:
        return "No LinkedInAPIClients in DB!"

    code = request.GET.get('code', '')
    state = request.GET.get('state', '')
    error = request.GET.get('error', '')

    if error:
        raise ValueError(error, request.GET.get('error_description', ''))

    if not str(api_client.state) == state:
        raise ValueError("State mismatch: api_client.state={}, request.state={}".format(
            api_client.state, state))

    params = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': api_client.redirect_uri,
        'client_id': api_client.client_id,
        'client_secret': api_client.client_secret
    }
    response = requests.post(url=settings.LINKEDIN_TOKEN_URL,
                             data=params)

    if response.status_code != 200:
        raise ValueError(response, response.content)

    response_data = response.json()
    api_client.access_token = response_data['access_token']
    api_client.expires_in = response_data['expires_in']
    api_client.save()

    return redirect(reverse('homepage:main-page', kwargs={'slug': 'main-page'}))
