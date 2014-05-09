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

"""Models for member app."""

from hashlib import md5

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from pdp.forum.models import Post, Topic
from pdp.tutorial.models import Tutorial
from pdp.article.models import Article


class Profile(models.Model):

    """Represents an user profile."""

    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    user = models.ForeignKey(User, unique=True, verbose_name=u'Utilisateur')

    site = models.CharField(u'Site internet', max_length=128, blank=True)
    show_email = models.BooleanField(u'Afficher adresse mail publiquement',
                                     default=True)

    avatar_url = models.CharField(
        u'URL de l\'avatar', max_length=128, null=True, blank=True
    )

    biography = models.TextField(u'Biographie', blank=True)

    def __unicode__(self):
        """Textual representation of a profile.

        Returns:
            string

        """
        return self.user.username

    def get_absolute_url(self):
        """Get URL to view this profile.

        Returns:
            string

        """
        return reverse('pdp.member.views.details', args=[self.user.username])

    def get_avatar_url(self):
        """Get the member's avatar URL.

        This will use custom URL or Gravatar.

        Returns:
            string

        """
        if self.avatar_url:
            return self.avatar_url
        else:
            return 'https://secure.gravatar.com/avatar/{0}?d=identicon'\
                .format(md5(self.user.email).hexdigest())

    def get_post_count(self):
        """Get total number of answers of the member on the forums.

        Returns:
            QuerySet on an integer.

        """
        return Post.objects.all().filter(author__pk=self.user.pk).count()

    def get_topic_count(self):
        """Get total number of topics created on the forums by the member.

        Returns:
            QuerySet on an integer.

        """
        return Topic.objects.all().filter(author=self.user).count()

    def get_followed_topics(self):
        """Get all the topics the user is currently following.

        Returns:
            QuerySet on Topic objects.

        """
        return Topic.objects.filter(topicfollowed__user=self.user)\
            .order_by('-last_message__pubdate')

    # Tutorial

    def get_tutorials(self):
        """Get all the tutorials written or being written by this member.

        Returns:
            QuerySet on Tutorial objects.

        """
        return Tutorial.objects.filter(authors=self.user.pk)

    def get_visible_tutorials(self):
        """Get all the tutorials published by this member.

        Returns:
            QuerySet on Tutorial objects.

        """
        return self.get_tutorials().filter(is_visible=True)

    def get_hidden_tutorials(self):
        """Get all the tutorials the member is currently writing.

        Returns:
            QuerySet on Tutorial objects.

        """
        return self.get_tutorials().filter(is_visible=False)

    # Article

    def get_articles(self):
        """Get all the articles written or being written by this member.

        Returns:
            QuerySet on Article objects.

        """
        return Article.objects.all().filter(author=self.user)

    def get_visible_articles(self):
        """Get all the articles published by this member.

        Returns:
            QuerySet on Article objects.

        """
        return self.get_articles().filter(is_visible=True)

    def get_hidden_articles(self):
        """Get all the articles the member is currently writing.

        Returns:
            QuerySet on Article objects.

        """
        return self.get_articles().filter(is_visible=False)
