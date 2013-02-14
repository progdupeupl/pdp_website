"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django_dynamic_fixture import G
from datetime import date
from pdp.article.models import *

""" List of assert methods on TestCase:
assertEqual(a, b)	      a == b	 
assertNotEqual(a, b)	    a != b	 
assertTrue(x)	          bool(x) is True	 
assertFalse(x)	          bool(x) is False	 
assertIs(a, b)	          a is b
assertIsNot(a, b)	      a is not b
assertIsNone(x)	          x is None
assertIsNotNone(x)	      x is not None
assertIn(a, b)	          a in b
assertNotIn(a, b)	        a not in b
assertIsInstance(a, b)	    isinstance(a, b)
assertNotIsInstance(a, b)	not isinstance(a, b)
"""

class ArticleTests(TestCase):
    def test_latest_articles_zero(self):
        """ Tests that the latest articles work if there are none. """
        self.assertEqual(0, len(get_last_articles()))

    def test_latest_articles_one(self):
        """ Tests that the latest articles work if there is only one. """
        article = G(Article, pubdate=date(2000,1,1))
        self.assertEqual(1, len(get_last_articles()))
        self.assertEqual(article, get_last_articles()[0])

    def test_latest_articles_four(self):
        """ Tests that the latest articles are sorted correctly"""
        a1 = G(Article, pubdate=date(2000,1,1))
        a2 = G(Article, pubdate=date(2001,1,1))
        a3 = G(Article, pubdate=date(2002,1,1))
        a4 = G(Article, pubdate=date(2003,1,1))

        last = get_last_articles()

        self.assertNotIn(a1, last)
        self.assertIn(a2, last)
        self.assertIn(a3, last)
        self.assertIn(a4, last)