# coding: utf-8

from django.test import TestCase

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from pdp.member.models import Profile


class MessagesIntegrationTests(TestCase):
    def test_url_index(self):
        resp = self.client.get(reverse('pdp.messages.views.index'))
        self.assertEquals(resp.status_code, 302)

    def test_url_new(self):
        resp = self.client.get(reverse('pdp.messages.views.new'))
        self.assertEquals(resp.status_code, 302)


class AuthenticatedMessagesIntegrationTests(TestCase):
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
        resp = self.client.get(reverse('pdp.messages.views.index'))
        self.assertEquals(resp.status_code, 200)

    def test_url_new(self):
        resp = self.client.get(reverse('pdp.messages.views.new'))
        self.assertEquals(resp.status_code, 200)

