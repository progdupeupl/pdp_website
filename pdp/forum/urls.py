# coding: utf-8

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',

    # Visualisation d'un sujet
    url(r'sujet/nouveau$', views.new),
    url(r'sujet/editer$', views.edit),
    url(r'sujet/(?P<topic_pk>\d+)-(?P<topic_slug>.+)$', views.topic),

    url(r'message/editer$', views.edit_post),
    url(r'message/nouveau$', views.anwser),
    url(r'message/utile$', views.useful_post),

    # Détails d'un forum
    url(r'(?P<cat_slug>.+)/(?P<forum_pk>\d+)-(?P<forum_slug>.+)/$', views.details),

    # Liste des forums d'une seule catégorie
    url(r'(?P<cat_pk>\d+)-(?P<cat_slug>.+)/$', views.cat_details),

   # Index
   url(r'$', views.index),
)
