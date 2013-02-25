# coding: utf-8

from pytz import utc
from datetime import datetime

from django.test import TestCase
from django.test.client import Client
from django_dynamic_fixture import G

from django.contrib.auth.models import User

from pdp.article.models import Article, get_last_articles


class ArticleTests(TestCase):
    def test_last_articles_zero(self):
        '''
        Tests that the last articles work if there are no visible articles.
        '''
        self.assertEqual(0, len(get_last_articles()))

        article = G(Article, is_visible=False)
        article  # to avoid unsused variable warning
        self.assertEqual(0, len(get_last_articles()))

    def test_last_articles_one(self):
        '''Tests that the last articles work if there is only one.'''
        article = G(Article, is_visible=True)
        self.assertEqual(1, len(get_last_articles()))
        self.assertEqual(article, get_last_articles()[0])

    def test_last_articles_many(self):
        '''Tests that the last articles work correctly'''
        articles = []
        for n in range(2000, 1900, -1):
            a = G(Article, pubdate=datetime(n, 1, 1, tzinfo=utc))
            articles.append(a)

        last = get_last_articles()

        for n, val in enumerate(last):
            self.assertEqual(val, articles[n])

    # Urls

    def test_url_index(self):
        client = Client()
        self.assertEqual(200, client.get('/articles/').status_code)

    def test_url_new(self):
        client = Client()

        # Check redirection if user not authenticated
        self.assertEqual(302, client.get('/articles/nouveau').status_code)

        # Check if user authenticated
        # TODO: log in with test user
        # self.assertEqual(200, client.get('/articles/nouveau').status_code)

    def test_url_view(self):
        client = Client()
        # Test for invisible article
        article = G(Article, is_visible=False)
        self.assertEqual(404,
                         client.get(article.get_absolute_url()).status_code)

        # Test for visible article
        article = G(Article, is_visible=True)
        self.assertEqual(200,
                         client.get(article.get_absolute_url()).status_code)
