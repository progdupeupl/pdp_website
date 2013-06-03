# coding: utf-8

from django.conf.urls import patterns, url

import views
import feeds

urlpatterns = patterns('',

    url(r'^flux/rss/$', feeds.LastTutorialsFeedRSS(),
        name='tutorial-feed-rss'),
    url(r'^flux/atom/$', feeds.LastTutorialsFeedATOM(),
        name='tutorial-feed-atom'),

# Viewing

    # TODO: Handle redirect

    url(r'^voir/(?P<tutorial_pk>\d+)-(?P<tutorial_slug>.+)/' +
    r'(?P<part_pos>\d+)-(?P<part_slug>.+)/' +
    r'(?P<chapter_pos>\d+)-(?P<chapter_slug>.+)$', views.view_chapter),

    url(r'^voir/(?P<tutorial_pk>\d+)-(?P<tutorial_slug>.+)/' +
    r'(?P<part_pos>\d+)-(?P<part_slug>.+)/$', views.view_part),

    # url(
    # r'^voir/(?P<tutorial_pk>\d+)-(?P<tutorial_slug>.+)/$',
    # views.view_tutorial),
    url(r'^(?P<tutorial_pk>\d+)/(?P<tutorial_slug>.+)/$',
        views.view_tutorial),

    url(r'^telecharger', views.download),

# Editing
    url(r'^editer/tutoriel$', views.edit_tutorial),
    url(r'^modifier/tutoriel$', views.modify_tutorial),
    url(r'^modifier/partie$', views.modify_part),
    url(r'^editer/partie$', views.edit_part),
    url(r'^modifier/chapitre$', views.modify_chapter),
    url(r'^editer/chapitre$', views.edit_chapter),
    url(r'^modifier/extrait$', views.modify_extract),
    url(r'^editer/extrait$', views.edit_extract),

# Adding
    url(r'^nouveau/tutoriel$', views.add_tutorial),
    url(r'^nouveau/partie$', views.add_part),
    url(r'^nouveau/chapitre$', views.add_chapter),
    url(r'^nouveau/extrait$', views.add_extract),

    url(r'^$', views.index),
)
