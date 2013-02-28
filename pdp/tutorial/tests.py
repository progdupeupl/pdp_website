# coding: utf-8

from django.test import TestCase
from django.test.client import Client
from django_dynamic_fixture import G

from pdp.tutorial.models import Tutorial, get_last_tutorials


class TutorialTests(TestCase):
    def test_last_tutorials_zero(self):
        '''
        Tests that the last articles work if there are no visible articles.
        '''
        self.assertEqual(0, len(get_last_tutorials()))

        tutorial = G(Tutorial, is_visible=False)
        tutorial  # to avoid unsused variable warning
        self.assertEqual(0, len(get_last_tutorials()))

    def test_last_tutorials_one(self):
        '''Tests that the last articles work if there is only one.'''
        article = G(Tutorial, is_visible=True)
        self.assertEqual(1, len(get_last_tutorials()))
        self.assertEqual(article, get_last_tutorials()[0])

    def test_last_articles_many(self):
        '''Tests that the last articles work correctly'''
        articles = []
        for n in range(2000, 1900, -1):
            a = G(Tutorial)
            articles.append(a)

        last = get_last_tutorials()

        for n, val in enumerate(last):
            self.assertEqual(val, articles[n])

    # Urls

    def test_url_index(self):
        '''Tests viewing the index page of tutorials'''
        client = Client()
        self.assertEqual(200, client.get('/tutoriels/').status_code)

    def test_url_new_tutorial(self):
        '''Tests adding a new tutorial as anonymous'''
        client = Client()
        self.assertEqual(302,
                         client.get('/tutoriels/nouveau/tutoriel').status_code)

    def test_url_view_tutorial_invisible(self):
        '''Testing viewing an invisible article as anonymous'''
        client = Client()
        article = G(Tutorial, is_visible=False)
        self.assertEqual(404,
                         client.get(article.get_absolute_url()).status_code)

    def test_url_view_tutorial_visible(self):
        '''Testing viewing a visible article as anonymous'''
        client = Client()
        article = G(Tutorial, is_visible=True)
        self.assertEqual(200,
                         client.get(article.get_absolute_url()).status_code)
