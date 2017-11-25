from django.conf.urls import url
from . import views


app_name = 'homepage'

urlpatterns = [
    url(r'^$',
        views.root),
    url(r'^(?P<slug>main-page)$',
        views.TextPageView.as_view(),
        name='main-page'),
    url(r'^(?P<slug>about)$',
        views.TextPageView.as_view(),
        name='about'),
    url(r'^(?P<slug>contact)$',
        views.TextPageView.as_view(),
        name='about'),
]
