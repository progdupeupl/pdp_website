# coding: utf-8

from django.test import TestCase
from django_dynamic_fixture import G

from django.contrib.auth.models import User

from pdp.member.models import Profile

from .paginator import paginator_range

from .templatetags.profile import profile
from .templatetags.interventions import interventions_topics


class TemplateTagsTests(TestCase):

    def test_profile_none(self):
        '''Test the output of profile templatetag if profile does not exist'''
        user = G(User)
        self.assertEqual(None, profile(user))

    def test_profile_existing(self):
        '''Test the output of profile templatetag if profile does exist'''
        user = G(User)
        p = G(Profile, user=user)
        self.assertEqual(p, profile(user))

    def test_interventions_none(self):
        '''
        Test both intervention_topics_count and interventions_topics
        templatetags when no topic should match.
        '''
        user = G(User)

        self.assertEqual(interventions_topics(user), {'unread': [],
                                                      'read': []})


class PaginatorRangeTests(TestCase):

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
