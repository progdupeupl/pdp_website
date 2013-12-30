# coding: utf-8

"""Tests for pages app."""

from django.test import TestCase
from django.test.client import Client


class PagesIntegrationTests(TestCase):

    """Integration tests without any specific instances."""

    def test_url_home(self):
        """Test if the index URL for the pages application is ok."""
        client = Client()
        self.assertEqual(200, client.get('/').status_code)
