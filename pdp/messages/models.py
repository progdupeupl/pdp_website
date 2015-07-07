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

"""Models for messages app."""

from math import ceil

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from pdp.utils import get_current_user


class PrivateTopic(models.Model):

    """Topic private, containing private posts."""

    class Meta:
        verbose_name = 'Message privé'
        verbose_name_plural = 'Messages privés'

    title = models.CharField('Titre', max_length=80)
    subtitle = models.CharField('Sous-titre', max_length=200, blank=True)

    author = models.ForeignKey(User, verbose_name=u'Auteur',
                               related_name='author')
    participants = models.ManyToManyField(User, verbose_name=u'Participants',
                                          related_name='participants')
    last_message = models.ForeignKey(u'PrivatePost', null=True, blank=True,
                                     related_name='last_message',
                                     verbose_name='Dernier message')
    pubdate = models.DateTimeField(u'Date de création', auto_now_add=True)

    def __str__(self):
        """Textual representation of a PrivateTopic object.

        Returns:
            string

        """
        return self.title

    def get_absolute_url(self):
        """Get URL to view the private topic.

        Returns:
            string

        """
        return reverse("pdp.messages.views.topic", kwargs={
            'topic_pk': self.pk,
            'topic_slug': slugify(self.title),
        })

    def get_post_count(self):
        """Get the number of private posts in the private topic.

        Returns:
            QuerySet on integer

        """
        return PrivatePost.objects.all()\
            .filter(privatetopic__pk=self.pk)\
            .count()

    def get_answer_count(self):
        """Get the number of answers in the private topic.

        Returns:
            Integer

        """
        return get_post_count() - 1

    def get_last_answer(self):
        """Gets the last answer in the thread, if any.

        Returns:
            PrivatePost object or None

        """

        try:
            last_post = PrivatePost.objects.all()\
                .filter(privatetopic__pk=self.pk)\
                .order_by('-pubdate')[0]
        except IndexError:
            return None

        # We do not want first post to be considered as an answer
        if last_post == self.first_post():
            return None
        else:
            return last_post

    def first_post(self):
        """Return the first post of a topic, written by topic's author.

        Returns:
            PrivatePost

        """
        return PrivatePost.objects\
            .filter(privatetopic=self)\
            .order_by('pubdate')[0]

    def last_read_post(self):
        """Return the last private post the user has read.

        Returns:
            PrivatePost object

        """
        try:
            post = PrivateTopicRead.objects\
                .select_related()\
                .filter(privatetopic=self, user=get_current_user())
            if len(post) == 0:
                return self.first_post()
            else:
                return post.latest('privatepost__pubdate').privatepost

        except PrivatePost.DoesNotExist:
            return self.first_post()

    def antispam(self, user=None):
        """Check if the user is allowed to post in a topic.

        This method uses the SPAM_LIMIT_SECONDS value. If user shouldn't be
        able to post, then antispam is activated and this method returns True.
        Otherwise time elapsed between user's last post and now is enough, and
        the method will return False.

        Returns:
            boolean

        """
        if user is None:
            user = get_current_user()

        last_user_privateposts = PrivatePost.objects\
            .filter(privatetopic=self)\
            .filter(author=user)\
            .order_by('-pubdate')

        if last_user_privateposts \
           and last_user_privateposts[0] == self.get_last_answer():
            last_user_privatepost = last_user_privateposts[0]
            t = timezone.now() - last_user_privatepost.pubdate
            if t.total_seconds() < settings.SPAM_LIMIT_SECONDS:
                return True

        return False

    def never_read(self):
        return never_privateread(self)


class PrivatePost(models.Model):

    """A private post written by an user."""

    privatetopic = models.ForeignKey(
        PrivateTopic, verbose_name=u'Message privé')
    author = models.ForeignKey(User, verbose_name=u'Auteur',
                               related_name='privateposts')
    text = models.TextField(u'Texte')

    pubdate = models.DateTimeField(u'Date de publication', auto_now_add=True)
    update = models.DateTimeField(u'Date d\'édition', null=True, blank=True)

    position_in_topic = models.IntegerField(u'Position dans le sujet')

    def __str__(self):
        """Textual representation of a PrivatePost object.

        Returns:
            string

        """
        return u'<Post pour "{0}", #{1}>'.format(self.privatetopic, self.pk)

    def get_absolute_url(self):
        """Get URL to view the private post.

        Returns:
            string

        """
        page = int(ceil(
            float(self.position_in_topic) / settings.POSTS_PER_PAGE
        ))

        return '{0}?page={1}#p{2}'\
            .format(self.privatetopic.get_absolute_url(), page, self.pk)


class PrivateTopicRead(models.Model):

    """Small model which keeps track of the user viewing private topics.

    It remembers the topic he looked and what was the last private Post at this
    time.

    """

    class Meta:
        verbose_name = 'Message privé lu'
        verbose_name_plural = 'Messages privés lus'

    privatetopic = models.ForeignKey(PrivateTopic)
    privatepost = models.ForeignKey(PrivatePost)
    user = models.ForeignKey(User, related_name='privatetopics_read')

    def __str__(self):
        """Textual representation of a PrivatePostRead object.

        Returns:
            string

        """
        return u'<Sujet "{0}" lu par {1}, #{2}>'.format(
            self.privatetopic, self.user, self.privatepost.pk)


def never_privateread(privatetopic, user=None):
    """Check if a private topic has been read by an user.

    Returns:
        boolean

    """
    if user is None:
        user = get_current_user()

    return PrivateTopicRead.objects\
        .filter(privatepost=privatetopic.last_message,
                privatetopic=privatetopic, user=user)\
        .count() == 0


def mark_read(privatetopic):
    """Mark a private topic as read for the user."""
    PrivateTopicRead.objects.filter(
        privatetopic=privatetopic, user=get_current_user()).delete()
    t = PrivateTopicRead(
        privatepost=privatetopic.last_message, privatetopic=privatetopic,
        user=get_current_user())
    t.save()


def get_last_privatetopics():
    """Get the 5 very last topics.

    Returns:
        List (or QuerySet?) of PrivateTopic objects

    """
    return PrivateTopic.objects.all().order_by('-pubdate')[:5]
