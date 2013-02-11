# coding: utf-8

from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',

    url(r'voir/(?P<user_name>.+)$', views.details),
    url(r'editer$', views.edit_profile),
    url(r'connexion$', views.login_view),
    url(r'deconnexion/$', views.logout_view),
    url(r'$', views.index),

)
