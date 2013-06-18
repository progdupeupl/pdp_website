# coding: utf-8

from django.test import TestCase
from django.test.client import Client
from django_dynamic_fixture import G

from pdp.tutorial.models import Tutorial, Part, get_last_tutorials


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

    # Current URL tests

    def test_url_index(self):
        '''Tests viewing the index page of tutorials'''
        resp = self.client.get('/tutoriels/')
        self.assertEqual(200, resp.status_code)

    def test_url_new_tutorial(self):
        '''Tests adding a new tutorial as anonymous'''
        resp = self.client.get('/tutoriels/nouveau/tutoriel')
        self.assertEqual(302, resp.status_code)

    def test_url_view_tutorial_invisible(self):
        '''Testing viewing an invisible tutorial as anonymous'''
        tutorial = G(Tutorial, is_visible=False)
        resp = self.client.get(tutorial.get_absolute_url())
        self.assertEqual(404, resp.status_code)

    def test_url_view_tutorial_visible(self):
        '''Testing viewing a visible tutorial as anonymous'''
        tutorial = G(Tutorial, is_visible=True)
        resp = self.client.get(tutorial.get_absolute_url())
        self.assertEqual(200, resp.status_code)

    def test_url_view_part_invisible(self):
        '''Testing viewing a part from invisible tutorial as anonymous'''
        tutorial = G(Tutorial, is_visible=False, is_mini=False)
        part = G(Part, tutorial=tutorial)
        resp = self.client.get(part.get_absolute_url())
        self.assertEqual(404, resp.status_code)

    def test_url_view_part_visible(self):
        '''Testing viewing a part from visible tutorial as anonymous'''
        tutorial = G(Tutorial, is_visible=True, is_mini=False)
        part = G(Part, tutorial=tutorial)
        resp = self.client.get(part.get_absolute_url())
        self.assertEqual(200, resp.status_code)

    # Deprecated URL redirect tests

    def test_url_deprecated_tutorial(self):
        tutorial = G(Tutorial, id=42, title='Test tutorial', is_visible=True)
        resp = self.client.get('/tutoriels/voir/42-test-tutorial/')
        self.assertRedirects(resp, tutorial.get_absolute_url(), 301)
