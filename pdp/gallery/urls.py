# coding: utf-8

from django.conf.urls import patterns, url

import views

urlpatterns = patterns('',
     # Viewing a gallery
    url(r'^nouveau$', views.new_gallery),
    url(r'^partager/(?P<gal_pk>\d+)$', views.share_gallery),
    url(r'^sup$', views.del_gallery),
    url(r'^(?P<gal_pk>\d+)/(?P<gal_slug>.+)', views.gallery_details),
    url(r'^$', views.gallery_list),
    url(r'^images/creer/(?P<gal_pk>\d+)$', views.new_image),
    url(r'^images/sup/(?P<gal_pk>\d+)$', views.del_image),
    url(r'^images/editer/(?P<gal_pk>\d+)/(?P<img_pk>\d+)$', views.edit_image),
)
