from django.conf.urls import url
from . import views
from .services import linkedin_api


app_name = 'homepage'

urlpatterns = [
    url(r'^$',
        views.root),
    url(r'^(?P<slug>main-page)$',
        views.TextPageView.as_view(),
        name='main-page'),
    url(r'^(?P<slug>about-me)$',
        views.TextPageView.as_view(),
        name='about-me'),
    url(r'^(?P<slug>career-bio)$',
        views.TextPageView.as_view(),
        name='career-bio'),

    url(r'^linkedin-auth$',
        linkedin_api.request_authorization_code,
        name='linkedin-auth'),
    url(r'^linkedin-callback$',
        linkedin_api.exchange_code_to_token,
        name='linkedin-callback'),
    url(r'^linkedin-get$',
        linkedin_api.get_profile_data,
        name='linkedin-get'),
]
