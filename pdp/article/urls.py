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

from pdp.article import views

urlpatterns = patterns(
    '',

    url(r'^flux/rss/$', views.redirect_feed_rss),
    url(r'^flux/atom/$', views.redirect_feed_atom),

    url(r'^(?P<article_pk>\d+)/(?P<article_slug>.+)$', views.redirect_view),

    url(r'^$', views.redirect_index),
)
