# coding: utf-8

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    # Viewing a thread
    url(r'^sujet/nouveau$', views.new),
    url(r'^sujet/editer$', views.edit),
    # url(r'sujet/(?P<topic_pk>\d+)-(?P<topic_slug>.+)$', views.topic),
    url(r'^sujet/(?P<topic_pk>\d+)/(?P<topic_slug>.+)$', views.topic),

    # Message-related
    url(r'^message/editer$', views.edit_post),
    url(r'^message/nouveau$', views.answer),
    url(r'^message/utile$', views.useful_post),
    
    # TODO: Handle redirect

    # Forum details
    # url(r'(?P<cat_slug>.+)/(?P<forum_pk>\d+)-(?P<forum_slug>.+)/$',
    #    views.details),
    
    url(r'^(?P<cat_slug>.+)/(?P<forum_slug>.+)/$',
        views.details),

    # Forums belonging to one category
    # url(r'(?P<cat_pk>\d+)-(?P<cat_slug>.+)/$', views.cat_details),
    url(r'^(?P<cat_slug>.+)/$', views.cat_details),

    # Home
    url(r'^$', views.index),
)
