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

from django.test import TestCase
from django.core.urlresolvers import reverse

from django_dynamic_fixture import G

from pdp.article.models import Article


class ArticleIntegrationTests(TestCase):
    def test_url_index(self):
        """Tests viewing the index page of articles."""
        resp = self.client.get(reverse('pdp.article.views.index'))
        self.assertEqual(301, resp.status_code)

    def test_url_view_invisible(self):
        """Testing viewing an invisible article as anonymous."""
        article = G(Article, is_visible=False)
        resp = self.client.get(article.get_absolute_url())
        self.assertEqual(403, resp.status_code)

    def test_url_view_visible(self):
        """Testing viewing a visible article as anonymous."""
        article = G(Article, is_visible=True)
        resp = self.client.get(article.get_absolute_url())
        self.assertEqual(301, resp.status_code)


class FeedsIntegrationTests(TestCase):
    def test_articles_feed_rss(self):
        resp = self.client.get('/articles/flux/rss/')
        self.assertEqual(resp.status_code, 301)

    def test_articles_feed_atom(self):
        resp = self.client.get('/articles/flux/atom/')
        self.assertEqual(resp.status_code, 301)
