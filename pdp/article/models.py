# coding: utf-8

from datetime import datetime

from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from pdp.utils import slugify


class Article(models.Model):

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    title = models.CharField('Titre', max_length=80)
    description = models.CharField('Description', max_length=200)

    text = models.TextField('Texte')

    author = models.ForeignKey(User, verbose_name='Auteur')
    pubdate = models.DateTimeField('Date de publication', blank=True)

    tags = TaggableManager()

    is_visible = models.BooleanField('Est visible publiquement')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/articles/{0}/{1}'.format(self.pk, slugify(self.title))

    def get_edit_url(self):
        return '/articles/editer?article={0}'.format(self.pk)


def get_last_articles():
    return Article.objects.all()\
        .filter(is_visible=True)\
        .order_by('-pubdate')[:3]


def get_prev_article(g_article):
    try:
        return Article.objects\
            .filter(is_visible=True)\
            .filter(pubdate__lt=g_article.pubdate)\
            .order_by('-pubdate')[0]
    except IndexError:
        return None


def get_next_article(g_article):
    try:
        return Article.objects\
            .filter(is_visible=True)\
            .filter(pubdate__gt=g_article.pubdate)\
            .order_by('pubdate')[0]
    except IndexError:
        return None
