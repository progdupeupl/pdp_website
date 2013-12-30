# coding: utf-8

"""Tests for utils app."""

import unittest

from django.contrib.auth.models import User
from django_dynamic_fixture import G

from pdp.member.models import Profile

from pdp.utils.templatetags.profile import profile
from pdp.utils.templatetags.interventions import interventions_topics

from pdp.utils.paginator import paginator_range


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
