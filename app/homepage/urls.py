from django.conf.urls import url
from . import views


app_name = 'homepage'

urlpatterns = [
    url(r'^(?P<slug>[-\w]+)',
        views.PageView.as_view(),
        name='view')
]
