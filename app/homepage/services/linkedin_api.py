from urllib.parse import urlencode, urlparse

import requests
from django.conf import settings
from django.shortcuts import redirect, reverse

from homepage.models import LinkedInAPIClient, LinkedInAPITextPage


def request_authorization_code(request):
    """
    Perform the second step of the OAuth2 dance for LinkedIn authentication, retrieving the authorization code for the client developer app.

    See the documentation at https://developer.linkedin.com/docs/oauth2
    """

    api_client = LinkedInAPIClient.objects.first()

    if not api_client:
        raise ValueError("No LinkedInAPIClients in DB!")

    params = {
        'response_type': 'code',
        'client_id': api_client.client_id,
        'redirect_uri': api_client.redirect_uri,
        'state': api_client.state,
    }

    url = "{}?{}".format(settings.LINKEDIN_AUTH_URL, urlencode(params))
    return redirect(url)


def exchange_code_to_token(request):
    """
    Perform the third step of the OAuth2 dance for LinkedIn authentication, exchanging the retrieved authorization code for an access token valid (atm) for 60 days.

    See the documentation at https://developer.linkedin.com/docs/oauth2
    """
    api_client = LinkedInAPIClient.objects.first()

    if not api_client:
        raise ValueError("No LinkedInAPIClients in DB!")

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

    if api_client.access_token:
        print("Refreshing Access Token")

    api_client.access_token = response_data['access_token']
    api_client.expires_in = response_data['expires_in']
    api_client.save()

    return redirect(reverse('homepage:linkedin-get'))


def get_profile_data(request):
    """
    Retrieve profile data to be persisted to the website's database. Explicitly retrieve the data as json.
    """
    api_client = LinkedInAPIClient.objects.first()

    if not api_client:
        raise ValueError("No LinkedInAPIClients in DB!")

    fields = '(id,headline,industry,summary,specialties,positions,public-profile-url)'

    url = settings.LINKEDIN_API_URL + 'people/~:{}'.format(fields)
    headers = {
        'Authorization': 'Bearer {}'.format(api_client.access_token),
        'x-li-format': 'json'
    }
    params = {'format': 'json'}

    response = requests.get(url=url, headers=headers, params=params)

    if response.status_code != 200:
        raise ValueError(response, response.content)

    data = response.json()

    career_page = LinkedInAPITextPage.objects.get(title='Career Bio')
    career_page.profile_id = data['id']
    career_page.headline = data['headline']
    career_page.industry = data['industry']
    career_page.summary = data['summary'].splitlines()[0]
    career_page.current_job_description = data['positions']['values'][0]['summary']
    career_page.profile_url = data['publicProfileUrl']
    career_page.save()

    print()

    return redirect(reverse('homepage:career-bio', kwargs={'slug': 'career-bio'}))
