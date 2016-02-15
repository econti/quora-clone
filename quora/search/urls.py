from django.conf.urls import patterns, include, url

from quora.search.views import (
    results
)


urlpatterns = [
    url(r'^results/$', results, name='results'),
]
