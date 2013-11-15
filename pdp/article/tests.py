# coding: utf-8

from pytz import utc

from datetime import datetime

from django.test import TestCase
from django.test.client import Client

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_dynamic_fixture import G
from django_dynamic_fixture.decorators import skip_for_database, SQLITE3

from pdp.article.models import Article, get_last_articles
from pdp.member.models import Profile


class GetLastArticlesTests(TestCase):
    '''Tests for the get_last_article function.'''

    def test_last_articles_zero(self):
        '''
        Tests that the last articles work if there are no visible articles.
        '''
        self.assertEqual(0, len(get_last_articles()))
        G(Article, is_visible=False)
        self.assertEqual(0, len(get_last_articles()))

    def test_last_articles_one(self):
        '''Tests that the last articles work if there is only one.'''
        article = G(Article, is_visible=True)
        self.assertEqual(1, len(get_last_articles()))
        self.assertEqual(article, get_last_articles()[0])

    @skip_for_database(SQLITE3)
    def test_last_articles_many(self):
        '''Tests that the last articles work correctly'''
        articles = []
        for n in range(2000, 1900, -1):
            a = G(Article, pubdate=datetime(n, 1, 1, tzinfo=utc))
            articles.append(a)

        last = get_last_articles()

        for n, val in enumerate(last):
            self.assertEqual(val, articles[n])


class ArticleIntegrationTests(TestCase):
    def test_url_index(self):
        '''Tests viewing the index page of articles.'''
        client = Client()
        self.assertEqual(200, client.get('/articles/').status_code)

    def test_url_new(self):
        '''Tests adding a new article as anonymous.'''
        client = Client()
        self.assertEqual(302, client.get('/articles/nouveau').status_code)

        # Check if user authenticated
        # TODO: log in with test user
        # self.assertEqual(200, client.get('/articles/nouveau').status_code)

    def test_url_view_invisible(self):
        '''Testing viewing an invisible article as anonymous.'''
        client = Client()
        article = G(Article, is_visible=False)
        self.assertEqual(404,
                         client.get(article.get_absolute_url()).status_code)

    def test_url_view_visible(self):
        '''Testing viewing a visible article as anonymous.'''
        client = Client()
        article = G(Article, is_visible=True)
        self.assertEqual(200,
                         client.get(article.get_absolute_url()).status_code)


class ArticleSearchIntegrationTests(TestCase):
    def setUp(self):
        self.user = G(User, username='test')
        self.profile = G(Profile, user=self.user)

    def test_url_search_none(self):
        resp = self.client.get(
            reverse('pdp.article.views.find_article',
                    args=[self.user.username]))

        self.assertEquals(resp.status_code, 200)

    def test_url_search_invisible(self):
        G(Article, is_visible=False, author=self.user)

        resp = self.client.get(
            reverse('pdp.article.views.find_article',
                    args=[self.user.username]))

        self.assertEquals(resp.status_code, 200)

    def test_url_search_visible(self):
        G(Article, is_visible=True, author=self.user)

        resp = self.client.get(
            reverse('pdp.article.views.find_article',
                    args=[self.user.username]))

        self.assertEquals(resp.status_code, 200)


class AuthenticatedArticleIntegrationTests(TestCase):
    def setUp(self):
        # Create user
        self.user = G(User, username='test')
        self.user.set_password('test')
        self.user.save()

        # Create profile
        self.profile = G(Profile, user=self.user)

        # Authenticate user
        self.client.login(username='test', password='test')

    def test_url_new(self):
        resp = self.client.get(reverse('pdp.article.views.new'))
        self.assertEquals(resp.status_code, 200)

    def test_url_edit(self):
        article = G(Article, author=self.user)
        resp = self.client.get(
            u'{}?article={}'.format(reverse('pdp.article.views.edit'),
                                    article.pk))
        self.assertEquals(resp.status_code, 200)

    def test_url_edit_badauthor(self):
        article = G(Article)
        resp = self.client.get(
            u'{}?article={}'.format(reverse('pdp.article.views.edit'),
                                    article.pk))
        self.assertEquals(resp.status_code, 404)

    def test_url_modify_get(self):
        resp = self.client.get(reverse('pdp.article.views.modify'))
        self.assertEquals(resp.status_code, 404)


class FeedsIntegrationTests(TestCase):

    def test_articles_feed_rss(self):
        resp = self.client.get('/articles/flux/rss/')
        self.assertEqual(resp.status_code, 200)

    def test_articles_feed_atom(self):
        resp = self.client.get('/articles/flux/atom/')
        self.assertEqual(resp.status_code, 200)
