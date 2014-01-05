# coding: utf-8

"""Tests for gallery app."""

from django.test import TestCase

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from pdp.member.models import Profile


class GalleryIntegrationTests(TestCase):

    """Integration tests with no specific valid instances."""

    def test_url_index(self):
        """Test to view gallery index as anonymous user."""
        resp = self.client.get(reverse('pdp.gallery.views.gallery_list'))
        self.assertEquals(302, resp.status_code)

    def test_url_new(self):
        """Test to create new gallery index as anonymous user."""
        resp = self.client.get(reverse('pdp.gallery.views.new_gallery'))
        self.assertEquals(302, resp.status_code)


class AuthenticatedGalleryIntegrationTests(TestCase):

    """Integration tests with logged-in user."""

    def setUp(self):
        # Create user
        self.user = G(User, username='test')
        self.user.set_password('test')
        self.user.save()

        # Create profile
        self.profile = G(Profile, user=self.user)

        # Authenticate user
        self.client.login(username='test', password='test')

    def test_url_index(self):
        """Test to view gallery index as logged-in user."""
        resp = self.client.get(reverse('pdp.gallery.views.gallery_list'))
        self.assertEquals(200, resp.status_code)

    def test_url_new(self):
        """Test to create new gallery index as logged-in user."""
        resp = self.client.get(reverse('pdp.gallery.views.new_gallery'))
        self.assertEquals(200, resp.status_code)
