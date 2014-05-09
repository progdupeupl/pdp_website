# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

"""Tests for gallery app."""

from django.test import TestCase
from django.core.urlresolvers import reverse

from django_dynamic_fixture import G
from pdp.utils.tests_helper import AuthenticatedTestCase

from pdp.gallery.models import Gallery, UserGallery, Image


class IntegrationTests(TestCase):

    """Integration tests with no specific valid instances."""

    def test_url_index(self):
        """Test to view gallery index as anonymous user."""
        resp = self.client.get(reverse('pdp.gallery.views.gallery_list'))
        self.assertEquals(302, resp.status_code)

    def test_url_new(self):
        """Test to create new gallery index as anonymous user."""
        resp = self.client.get(reverse('pdp.gallery.views.new_gallery'))
        self.assertEquals(302, resp.status_code)


class AuthenticatedntegrationTests(AuthenticatedTestCase):

    """Integration tests with logged-in user."""

    def test_url_index(self):
        """Test to view gallery index as logged-in user."""
        resp = self.client.get(reverse('pdp.gallery.views.gallery_list'))
        self.assertEquals(200, resp.status_code)

    def test_url_new(self):
        """Test to create new gallery index as logged-in user."""
        resp = self.client.get(reverse('pdp.gallery.views.new_gallery'))
        self.assertEquals(200, resp.status_code)


class AuthenticatedGalleryTestCase(AuthenticatedTestCase):
    def setUp(self):
        AuthenticatedTestCase.setUp(self)

        self.gallery = G(Gallery, title='test', slug='test')
        self.usergallery = G(UserGallery, user=self.user, gallery=self.gallery)


class AuthenticatedGalleryIntegrationTests(AuthenticatedGalleryTestCase):

    """Integration tests with logged-in user and existing gallery."""

    def test_url_new_image(self):
        resp = self.client.get(reverse('pdp.gallery.views.new_image',
                                       args=(str(self.gallery.pk))))
        self.assertEquals(200, resp.status_code)


class AuthenticatedImageIntegrationTests(AuthenticatedGalleryTestCase):
    def setUp(self):
        AuthenticatedGalleryTestCase.setUp(self)

        self.image = G(Image, gallery=self.gallery)

    def test_url_edit_image(self):
        resp = self.client.get(reverse('pdp.gallery.views.edit_image',
                                       args=(str(self.gallery.pk),
                                             str(self.image.pk))))
        self.assertEquals(200, resp.status_code)
