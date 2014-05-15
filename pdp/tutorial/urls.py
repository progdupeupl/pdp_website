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

from pdp.tutorial import views
from pdp.tutorial import feeds

urlpatterns = patterns(
    '',

    url(r'^flux/rss/$', feeds.LastTutorialsFeedRSS(),
        name='tutorial-feed-rss'),
    url(r'^flux/atom/$', feeds.LastTutorialsFeedATOM(),
        name='tutorial-feed-atom'),

    # Viewing

    # Current URLs
    url(r'^auteur/(?P<name>.+)$', views.by_author),
    url(r'^categorie/(?P<name>.+)$', views.by_category),

    url(r'^(?P<tutorial_pk>\d+)/(?P<tutorial_slug>.+)/'
        r'(?P<part_slug>.+)/'
        r'(?P<chapter_slug>.+)/$',
        views.view_chapter, name="view-chapter-url"),

    url(r'^(?P<tutorial_pk>\d+)/(?P<tutorial_slug>.+)/'
        r'(?P<part_slug>.+)/$', views.view_part, name="view-part-url"),

    url(r'^(?P<tutorial_pk>\d+)/(?P<tutorial_slug>.+)/$',
        views.view_tutorial, name="view-tutorial-url"),

    url(r'^telecharger$', views.download),

    # Editing

    url(r'^editer/tutoriel$', views.edit_tutorial),
    url(r'^modifier/tutoriel$', views.modify_tutorial),
    url(r'^modifier/partie$', views.modify_part),
    url(r'^editer/partie$', views.edit_part),
    url(r'^modifier/chapitre$', views.modify_chapter),
    url(r'^editer/chapitre$', views.edit_chapter),
    url(r'^modifier/extrait$', views.modify_extract),
    url(r'^editer/extrait$', views.edit_extract),

    # Adding

    url(r'^nouveau/tutoriel$', views.add_tutorial),
    url(r'^nouveau/partie$', views.add_part),
    url(r'^nouveau/chapitre$', views.add_chapter),
    url(r'^nouveau/extrait$', views.add_extract),

    url(r'^$', views.index),
)
