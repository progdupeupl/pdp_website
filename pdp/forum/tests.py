# coding: utf-8

from django.test import TestCase
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from pdp.member.models import Profile
from pdp.forum.models import Category, Forum, Topic, Post


class ForumIntegrationTests(TestCase):

    def test_index_url(self):
        '''
        Tests if the index URL of the forum application ('/forums/') is ok.
        '''
        resp = self.client.get('/forums/')
        self.assertEqual(resp.status_code, 200)


class ForumCategoryIntegrationTests(TestCase):

    def setUp(self):
        self.category = G(Category, id=42, title='Test category',
                          slug='test-category')

    def test_category_url(self):
        resp = self.client.get(self.category.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_deprecated_category_url_redirect(self):
        resp = self.client.get('/forums/42-test-category/')
        self.assertRedirects(resp, self.category.get_absolute_url(), 301)


class ForumForumIntegrationTests(TestCase):

    def setUp(self):
        self.category = G(Category, id=42, title='Test category',
                          slug='test-category')
        self.forum = G(Forum, id=21, title='Test forum', slug='test-forum',
                       category=self.category)

    def test_forum_url(self):
        resp = self.client.get(self.forum.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_deprecated_forum_url_redirect(self):
        resp = self.client.get('/forums/42-test-category/21-test-forum/')
        self.assertRedirects(resp, self.forum.get_absolute_url(), 301)


def ForumTopicIntegrationTests(TestCase):

    def setUp(self):
        # Author
        self.author = G(User, username='test')
        self.author_profile = G(Profile, user=self.user)

        # Forum and category
        self.category = G(Category, id=42, title='Test category',
                          slug='test-category')
        self.forum = G(Forum, id=21, title='Test forum', slug='test-forum',
                       category=self.category)

        # Topic
        self.topic = G(Topic, id=112, title='Test subject',
                       slug='test-subject', forum=self.forum,
                       author=self.author)

        # Post
        self.post = G(Post, author=self.author, text='Test')

    def test_topic_url(self):
        resp = self.client.get(self.topic.get_absolute_url())
        self.assertEqual(resp.status_code, 200)

    def test_deprecated_topic_url_redirect(self):
        resp = self.client.get('/forums/sujet/112-test-topic')
        self.assertRedirects(resp, self.topic.get_absolute_url(), 301)


class FeedsIntegrationTests(TestCase):

    def test_messages_feed_rss(self):
        resp = self.client.get('/forums/flux/messages/rss/')
        self.assertEquals(resp.status_code, 200)

    def test_messages_feed_atom(self):
        resp = self.client.get('/forums/flux/messages/atom/')
        self.assertEquals(resp.status_code, 200)

    def test_topics_feed_rss(self):
        resp = self.client.get('/forums/flux/sujets/rss/')
        self.assertEquals(resp.status_code, 200)

    def test_topics_feed_atom(self):
        resp = self.client.get('/forums/flux/sujets/atom/')
        self.assertEquals(resp.status_code, 200)

    def test_deprecated_feeds_redirect_rss(self):
        resp = self.client.get('/forums/flux/rss/')
        self.assertRedirects(resp, '/forums/flux/messages/rss/', 301)

    def test_deprecated_feeds_redirect_atom(self):
        resp = self.client.get('/forums/flux/atom/')
        self.assertRedirects(resp, '/forums/flux/messages/atom/', 301)
