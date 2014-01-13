# coding: utf-8

from django.conf.urls import patterns, url

from pdp.member import views

urlpatterns = patterns(
    '',

    # Profile
    url(r'^voir/(?P<user_name>.+)$', views.details),
    url(r'^profil/editer$', views.edit_profile),

    # User's actions
    url(r'^publications$', views.publications),
    url(r'^actions$', views.actions),

    # Settings
    url(r'^parametres/profil$', views.settings_profile),
    url(r'^parametres/compte$', views.settings_account),

    url(r'^connexion$', views.login_view),
    url(r'^inscription$', views.register_view),
    url(r'^deconnexion/$', views.logout_view),
    url(r'^$', views.index),
)
