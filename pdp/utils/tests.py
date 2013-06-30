# coding: utf-8

from django.test import TestCase
from django_dynamic_fixture import G

from django.contrib.auth.models import User

from pdp.member.models import Profile

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
