# coding: utf-8

from django.test import TestCase
from django_dynamic_fixture import G

from django.contrib.auth.models import User

from .models import Category, Forum, Topic, Post

class ForumTests(TestCase):
    def test_index_url(self):
        '''
        Tests if the index URL of the forum application ('/forums/') is ok.
        '''
        resp = self.client.get('/forums/')
        self.assertEqual(resp.status_code, 200)

    def test_category_url(self):
        '''
        Test if the URL assiociated with a category is ok.
        '''
        category = G(Category, pk=42, name='Test category')

        resp = self.client.get('/forums/42-test-category')
        self.assertEqual(resp.status_code, 200)
