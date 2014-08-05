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

"""Tests for utils app."""

import unittest
import hashlib

from django.contrib.auth.models import User
from django_dynamic_fixture import G

from pdp.member.models import Profile

from pdp.utils.templatetags.profile import profile
from pdp.utils.templatetags.interventions import interventions_topics

from pdp.utils.paginator import paginator_range
from pdp.utils import mail


class TemplateTagsTests(unittest.TestCase):

    """Test for the custom template tags about users."""

    def setUp(self):
        self.user = G(User)

    def test_profile_none(self):
        """Test the output of profile templatetag if profile does not exist."""
        self.assertEqual(None, profile(self.user))

    def test_profile_existing(self):
        """Test the output of profile templatetag if profile does exist."""
        p = G(Profile, user=self.user)
        self.assertEqual(p, profile(self.user))

    def test_interventions_none(self):
        """Test templatetags when no topic should match."""
        self.assertEqual(interventions_topics(self.user), {'unread': [],
                                                           'read': []})


class PaginatorRangeTests(unittest.TestCase):

    """Tests for the paginator_range function."""

    def test_out_of_range(self):
        self.assertRaises(ValueError, lambda: paginator_range(3, 2))

    def test_one(self):
        result = paginator_range(1, 1)
        self.assertEqual(result, [1])

    def test_small(self):
        result = paginator_range(2, 3)
        self.assertEqual(result, [1, 2, 3])

    def test_small_limit(self):
        result = paginator_range(1, 4)
        self.assertEqual(result, [1, 2, 3, 4])

    def test_big_start(self):
        result = paginator_range(1, 10)
        self.assertEqual(result, [1, 2, None, 10])

    def test_big_start_limit(self):
        result = paginator_range(3, 10)
        self.assertEqual(result, [1, 2, 3, 4, None, 10])

    def test_big_middle(self):
        result = paginator_range(5, 10)
        self.assertEqual(result, [1, None, 4, 5, 6, None, 10])

    def test_big_end(self):
        result = paginator_range(10, 10)
        self.assertEqual(result, [1, None, 9, 10])

    def test_big_end_limit(self):
        result = paginator_range(7, 10)
        self.assertEqual(result, [1, None, 6, 7, 8, 9, 10])

class MailTests(unittest.TestCase):

    """Tests for the mail utilities."""

    def test_send_templated_mail(self):
        recipients = ['test1@localhost']

        result = mail.send_templated_mail(
            subject='Fake subject',
            template='base.txt',
            context={},
            recipients=recipients
        )

        self.assertEqual(result, 1)

    def test_send_mail_to_confirm_registration(self):
        recipients = ['test1@localhost']

        result = mail.send_mail_to_confirm_registration(
            user=G(User, username='Blaireau1', email='test1@localhost'),
            link=hashlib.sha1('blbl'.encode('ascii')).hexdigest()
        )

        self.assertEqual(result, 1)
