# coding: utf-8

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
    # Deprecated URLs, have to be checked before new ones to avoid conflict
    url(r'^sujet/(?P<topic_pk>\d+)-(?P<topic_slug>.+)$',
        views.deprecated_topic_redirect),
    url(r'^(?P<cat_slug>.+)/(?P<forum_pk>\d+)-(?P<forum_slug>.+)/$',
        views.deprecated_details_redirect),
    url(r'^(?P<cat_pk>\d+)-(?P<cat_slug>.+)/$',
        views.deprecated_cat_details_redirect),


    # Viewing a thread
    url(r'^sujet/nouveau$', views.new),
    url(r'^sujet/editer$', views.edit),
    url(r'^sujet/(?P<topic_pk>\d+)/(?P<topic_slug>.+)$', views.topic),

    # Message-related
    url(r'^message/editer$', views.edit_post),
    url(r'^message/nouveau$', views.answer),
    url(r'^message/utile$', views.useful_post),
    
    # Forum details
    
    url(r'^(?P<cat_slug>.+)/(?P<forum_slug>.+)/$',
        views.details),

    # Forums belonging to one category
    url(r'^(?P<cat_slug>.+)/$', views.cat_details),

    # Home
    url(r'^$', views.index),  
)
