# coding: utf-8

"""Tests for pages app."""

from django.test import TestCase

from django.core.urlresolvers import reverse


class PagesIntegrationTests(TestCase):

    """Integration tests without any specific instances."""

    # Misc tests for useful urls

    def test_url_home(self):
        """Test if the index URL for homepage is ok."""
        resp = self.client.get(reverse('pdp.pages.views.home'))
        self.assertEquals(200, resp.status_code)

    def test_url_robots(self):
        resp = self.client.get(reverse('pdp.pages.views.robots'))
        self.assertEquals(200, resp.status_code)

    # Really page-related tests

    def test_url_page_index(self):
        """Test if the index URL for the pages application is ok."""
        resp = self.client.get(reverse('pdp.pages.views.index'))
        self.assertEquals(200, resp.status_code)

    def test_url_page_about(self):
        resp = self.client.get(reverse('pdp.pages.views.about'))
        self.assertEquals(200, resp.status_code)

    def test_url_page_help_markdown(self):
        resp = self.client.get(reverse('pdp.pages.views.help_markdown'))
        self.assertEquals(200, resp.status_code)

    def test_url_page_help_writting(self):
        resp = self.client.get(reverse('pdp.pages.views.help_writting'))
        self.assertEquals(200, resp.status_code)
