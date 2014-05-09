# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, url

from pdp.gallery import views

urlpatterns = patterns(
    '',

    # Viewing a gallery
    url(r'^nouveau$', views.new_gallery),
    url(r'^modifier$', views.modify_gallery),

    url(r'^(?P<gal_pk>\d+)/(?P<gal_slug>.+)', views.gallery_details),
    url(r'^$', views.gallery_list),

    # Image-related
    url(r'^image/ajouter/(?P<gal_pk>\d+)$', views.new_image),
    url(r'^image/modifier$', views.modify_image),
    url(r'^image/editer/(?P<gal_pk>\d+)/(?P<img_pk>\d+)$', views.edit_image),
)
