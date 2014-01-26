# coding: utf-8

"""An helper for writing tests faster."""

from django.test import TestCase
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from pdp.member.models import Profile


class AuthenticatedTestCase(TestCase):
    def setUp(self):
        # Create user
        self.user = G(User, username='test')
        self.user.set_password('test')
        self.user.save()

        # Create profile
        self.profile = G(Profile, user=self.user)

        # Authenticate user
        self.client.login(username='test', password='test')
