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

from pdp.forum import views
from pdp.forum import feeds

urlpatterns = patterns(
    '',

    # Feeds
    url(r'^flux/rss/$', views.deprecated_feed_messages_rss),
    url(r'^flux/atom/$', views.deprecated_feed_messages_atom),

    url(r'^flux/messages/rss/$', feeds.LastPostsFeedRSS(),
        name='post-feed-rss'),
    url(r'^flux/messages/atom/$', feeds.LastPostsFeedATOM(),
        name='post-feed-atom'),

    url(r'^flux/sujets/rss/$', feeds.LastTopicsFeedRSS(),
        name='topic-feed-rss'),
    url(r'^flux/sujets/atom/$', feeds.LastTopicsFeedATOM(),
        name='topic-feed-atom'),

    # Deprecated URLs, have to be checked before new ones to avoid conflict
    url(r'^sujet/(?P<topic_pk>\d+)-(?P<topic_slug>.+)$',
        views.deprecated_topic_redirect),
    url(r'^(?P<cat_slug>.+)/(?P<forum_pk>\d+)-(?P<forum_slug>.+)/$',
        views.deprecated_details_redirect),
    url(r'^(?P<cat_pk>\d+)-(?P<cat_slug>.+)/$',
        views.deprecated_cat_details_redirect),

    # Viewing a thread
    url(r'^sujet/nouveau$', views.new),
    url(r'^sujet/editer$', views.edit),
    url(r'^sujet/(?P<topic_pk>\d+)/(?P<topic_slug>.+)$', views.topic),
    url(r'^sujets/(?P<name>.+)', views.find_topic),

    # Message-related
    url(r'^message/editer$', views.edit_post),
    url(r'^message/nouveau$', views.answer),
    url(r'^message/utile$', views.useful_post),
    url(r'^messages/(?P<name>.+)$', views.find_post),

    # Forum details
    url(r'^(?P<cat_slug>.+)/(?P<forum_slug>.+)/$',
        views.details),

    # Forums belonging to one category
    url(r'^(?P<cat_slug>.+)/$', views.cat_details),

    # Home
    url(r'^$', views.index),

    # Followed topics
    url(r'^suivis$', views.followed_topics),
)
