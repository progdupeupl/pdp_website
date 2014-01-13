# coding: utf-8

from django.conf.urls import patterns, url

from pdp.pages import views

urlpatterns = patterns(
    '',

    # Markdown helper
    url(r'^markdown$', views.help_markdown),
    url(r'^apropos$', views.about),

    url(r'^$', views.index),
)
