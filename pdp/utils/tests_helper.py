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
