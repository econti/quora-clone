from django.conf.urls import patterns, include, url

from quora.questions.views import (
    drafts,
    edit,
    comment,
    preview,
    question,
    questions,
    tag,
    vote,
    write,
)


urlpatterns = [
    url(r'^$', questions, name='questions'),
    url(r'^write/$', write, name='write'),
    url(r'^preview/$', preview, name='preview'),
    url(r'^drafts/$', drafts, name='drafts'),
    url(r'^comment/$', comment, name='comment'),
    url(r'^vote/$', vote, name='vote'),
    url(r'^tag/(?P<tag_name>.+)/$', tag, name='tag'),
    url(r'^edit/(?P<id>\d+)/$', edit, name='edit_question'),
    url(r'^(?P<slug>[-\w]+)/$', question, name='question'),
]
