# coding: utf-8

"""Tests for gallery app."""

from django.test import TestCase


class GalleryIntegrationTests(TestCase):

    """Integration tests with no specific valid instances."""

    def test_index_anon(self):
        """Test to view gallery index as anonymous user."""
        resp = self.client.get('/galerie/')
        self.assertEquals(302, resp.status_code)
