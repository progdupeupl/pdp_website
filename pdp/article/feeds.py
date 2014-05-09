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

from django.core.cache import cache

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from pdp.article.models import Article


class LastArticlesFeedRSS(Feed):
    title = "Articles sur Progdupeupl"
    link = "/articles/"
    description = "Les derniers articles parus sur Progdupeupl."

    def items(self):
        articles = cache.get('latest_articles')

        if articles is None:
            articles = Article.objects\
                .filter(is_visible=True)\
                .order_by('-pubdate')[:5]

            cache.set('latest_articles', articles)

        return articles

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_author_name(self, item):
        return item.author.username

    def item_author_link(self, item):
        return item.author.get_absolute_url()

    def item_link(self, item):
        return item.get_absolute_url()


class LastArticlesFeedATOM(LastArticlesFeedRSS):
    feed_type = Atom1Feed
    subtitle = LastArticlesFeedRSS.description
