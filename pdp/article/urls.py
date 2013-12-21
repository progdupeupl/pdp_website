# coding: utf-8

from django.conf.urls import patterns, url

import views
import feeds

urlpatterns = patterns('',
    url(r'^flux/rss/$', feeds.LastArticlesFeedRSS(), name='article-feed-rss'),
    url(r'^flux/atom/$', feeds.LastArticlesFeedATOM(),
        name='article-feed-atom'),

    # TODO: Handle redirect

    url(r'^voir/(?P<article_pk>\d+)-(?P<article_slug>.+)$',
        views.deprecated_view_redirect),
    url(r'^(?P<article_pk>\d+)/(?P<article_slug>.+)$', views.view),

    url(r'^telecharger', views.download),

    url(r'^nouveau$', views.new),
    url(r'^editer$', views.edit),
    url(r'^modifier$', views.modify),
    url(r'^(?P<name>.+)$', views.find_article),

    url(r'^$', views.index),
)
