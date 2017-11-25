from django.conf.urls import url
from . import views


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
    url(r'^(?P<slug>contact)$',
        views.TextPageView.as_view(),
        name='contact'),
]
