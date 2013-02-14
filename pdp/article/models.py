# coding: utf-8

from django.db import models
from django.contrib.auth.models import User

from pdp.utils import slugify

class Article(models.Model):
    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    title = models.CharField('Titre', max_length=80)
    description = models.CharField('Description', max_length=200)

    text = models.TextField('Texte')

    author = models.ForeignKey(User, verbose_name='Auteur')
    pubdate = models.DateTimeField('Date de création', auto_now_add=True)

    is_visible = models.BooleanField('Est visible publiquement')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/articles/voir/%s-%s' % (self.pk, slugify(self.title))

def get_last_articles():
    return Article.objects.all().order_by('-pubdate')[:3]
