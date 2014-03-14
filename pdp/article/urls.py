# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

from django.conf.urls import patterns, url

from pdp.article import views
from pdp.article import feeds

urlpatterns = patterns(
    '',

    url(r'^flux/rss/$', feeds.LastArticlesFeedRSS(), name='article-feed-rss'),
    url(r'^flux/atom/$', feeds.LastArticlesFeedATOM(),
        name='article-feed-atom'),

    # TODO: Handle redirect

    url(r'^voir/(?P<article_pk>\d+)-(?P<article_slug>.+)$',
        views.deprecated_view_redirect),
    url(r'^(?P<article_pk>\d+)/(?P<article_slug>.+)$', views.view),

    url(r'^telecharger$', views.download),

    url(r'^nouveau$', views.new),
    url(r'^editer$', views.edit),
    url(r'^modifier$', views.modify),
    url(r'^auteur/(?P<name>.+)$', views.find_article),

    url(r'^tags/$', views.tags),
    url(r'^tag/(?P<name>.+)$', views.tag),

    url(r'^$', views.index),
)
