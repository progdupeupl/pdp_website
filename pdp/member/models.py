# coding: utf-8

from hashlib import md5

from django.db import models
from django.contrib.auth.models import User

from pdp.forum.models import Post, Topic
from pdp.tutorial.models import Tutorial
from pdp.article.models import Article


class Profile(models.Model):
    '''Represents an user profile'''
    class Meta:
        verbose_name = 'Profil'
        verbose_name_plural = 'Profils'

    user = models.ForeignKey(User, unique=True, verbose_name='Utilisateur')

    site = models.CharField('Site internet', max_length=128, blank=True)
    show_email = models.BooleanField('Afficher adresse mail publiquement',
                                     default=True)

    biography = models.TextField('Biographie', blank=True)

    def __unicode__(self):
        '''Textual forum of a profile'''
        return self.user.username

    def get_absolute_url(self):
        '''Absolute URL to the profile page'''
        return '/membres/voir/%s' % self.user.username

    def get_gravatar_url(self):
        '''Avatar URL (using Gravatar)'''
        return 'http://gravatar.com/avatar/%s?d=identicon' % md5(self.user.email).hexdigest()

    def get_post_count(self):
        '''Number of messages posted'''
        return Post.objects.all().filter(author__pk=self.user.pk).count()

    def get_topic_count(self):
        '''Number of threads created'''
        return Topic.objects.all().filter(author=self.user).count()

    # Tutorial

    def get_tutorials(self):
        return Tutorial.objects.filter(authors=self.user.pk)

    def get_visible_tutorials(self):
        return self.get_tutorials().filter(is_visible=True)

    def get_hidden_tutorials(self):
        return self.get_tutorials().filter(is_visible=False)

    # Article

    def get_articles(self):
        return Article.objects.all().filter(author=self.user)

    def get_visible_articles(self):
        return self.get_articles().filter(is_visible=True)

    def get_hidden_articles(self):
        return self.get_articles().filter(is_visible=False)
