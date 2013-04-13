# coding: utf-8

from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    # Markdown helper (fallback and AJAX)
    url(r'aide-markdown$', views.help_markdown),
    url(r'aide-markdown.ajax$', views.help_markdown_ajax),
)
