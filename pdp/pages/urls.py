# coding: utf-8

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',

    # Markdown helper (fallback and AJAX)
    url(r'^markdown$', views.help_markdown),
    url(r'^markdown.ajax$', views.help_markdown_ajax),

    url(r'^$', views.index),
)
