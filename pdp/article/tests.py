from django.test import TestCase
from django_dynamic_fixture import G
from pytz import utc
from datetime import *
from pdp.article.models import *

class ArticleTests(TestCase):
    def test_latest_articles_zero(self):
        """ Tests that the latest articles work if there are none. """
        self.assertEqual(0, len(get_last_articles()))

    def test_latest_articles_one(self):
        """ Tests that the latest articles work if there is only one. """
        article = G(Article, pubdate=datetime(2000,1,1,tzinfo=utc))
        self.assertEqual(1, len(get_last_articles()))
        self.assertEqual(article, get_last_articles()[0])

    def test_latest_articles_many(self):
        """ Tests that the latest articles work correctly"""
        articles = []
        for n in range(2000, 1900, -1):
            a = G(Article, pubdate=datetime(n,1,1,tzinfo=utc))
            articles.append(a)
        
        last = get_last_articles()

        for n, val in enumerate(last):
            self.assertEqual(val, articles[n])