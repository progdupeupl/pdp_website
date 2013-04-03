# coding: utf-8

from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'voir/(?P<article_pk>\d+)-(?P<article_slug>.+)$', views.view),
    url(r'nouveau$', views.new),
    url(r'editer$', views.edit),
    url(r'modifier$', views.modify),

    url(r'$', views.index),
)
