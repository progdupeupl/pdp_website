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

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from pdp.member.models import Profile


class MemberIntegrationTests(TestCase):

    def test_index(self):
        resp = self.client.get(reverse('pdp.member.views.index'))
        self.assertEqual(resp.status_code, 200)

    def test_details(self):
        user = G(User, username='toto')
        G(Profile, user=user)

        resp = self.client.get(reverse('pdp.member.views.details',
                               args=[user.username]))
        self.assertEqual(resp.status_code, 200)

    def test_register(self):
        resp = self.client.get(reverse('pdp.member.views.register_view'))
        self.assertEqual(resp.status_code, 200)

    def test_login(self):
        resp = self.client.get(reverse('pdp.member.views.login_view'))
        self.assertEqual(resp.status_code, 200)

    def test_login_user(self):
        user = G(User, username='test')
        user.set_password('test')
        user.save()

        G(Profile, user=user)

        self.client.post(reverse('pdp.member.views.login_view'),
                         {'username': 'test',
                          'password': 'test'})

        self.assertEqual(self.client.session['_auth_user_id'], user.pk)


class AuthenticatedMemberIntegrationTests(TestCase):

    def setUp(self):
        # Create user
        self.user = G(User, username='test')
        self.user.set_password('test')
        self.user.save()

        # Create profile
        self.profile = G(Profile, user=self.user)

        # Authenticate user
        self.client.login(username='test', password='test')

    def test_settings_profile(self):
        resp = self.client.get(reverse('pdp.member.views.settings_profile'))
        self.assertEqual(resp.status_code, 200)

    def test_settings_account(self):
        resp = self.client.get(reverse('pdp.member.views.settings_account'))
        self.assertEqual(resp.status_code, 200)

    def test_publications(self):
        resp = self.client.get(reverse('pdp.member.views.publications'))
        self.assertEqual(resp.status_code, 200)

    def test_actions(self):
        resp = self.client.get(reverse('pdp.member.views.actions'))
        self.assertEqual(resp.status_code, 200)

    def test_disconnect(self):
        resp = self.client.get(reverse('pdp.member.views.logout_view'))
        self.assertEquals(resp.status_code, 200)
