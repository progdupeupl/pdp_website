# coding: utf-8

import os
import string
from django.db import models
from django.contrib.auth.models import User

from taggit.managers import TaggableManager

from pdp.utils import slugify

from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile

IMAGE_MAX_WIDTH = 64
IMAGE_MAX_HEIGHT = 64


def image_path(instance, filename):
    '''Return path to an image'''
    ext = filename.split('.')[-1]
    filename = u'original.{}'.format(string.lower(ext))
    return os.path.join('articles', str(instance.pk), filename)


def thumbnail_path(instance, filename):
    '''Return path to a thumbnail'''
    ext = filename.split('.')[-1]
    filename = u'thumb.{}'.format(string.lower(ext))
    return os.path.join('articles', str(instance.pk), filename)


class Article(models.Model):

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

    title = models.CharField('Titre', max_length=80)
    description = models.CharField('Description', max_length=200)

    text = models.TextField('Texte')

    author = models.ForeignKey(User, verbose_name='Auteur',
                               related_name='articles')
    pubdate = models.DateTimeField('Date de publication', blank=True)

    tags = TaggableManager()

    image = models.ImageField(upload_to=image_path,
                              blank=True, null=True, default=None)
    thumbnail = models.ImageField(upload_to=thumbnail_path,
                                  blank=True, null=True, default=None)

    is_visible = models.BooleanField('Est visible publiquement')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return '/articles/{0}/{1}'.format(self.pk, slugify(self.title))

    def get_edit_url(self):
        return '/articles/editer?article={0}'.format(self.pk)

    def save(self, force_update=False, force_insert=False,
             thumb_size=(IMAGE_MAX_HEIGHT, IMAGE_MAX_WIDTH)):

        if has_changed(self, 'image') and self.image:
            # TODO : delete old image

            image = Image.open(self.image)

            if image.mode not in ('L', 'RGB'):
                image = image.convert('RGB')

            image.thumbnail(thumb_size, Image.ANTIALIAS)

            # save the thumbnail to memory
            temp_handle = StringIO()
            image.save(temp_handle, 'png')
            temp_handle.seek(0)  # rewind the file

            # save to the thumbnail field
            suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
                                     temp_handle.read(),
                                     content_type='image/png')
            self.thumbnail.save('{}.png'.format(suf.name), suf, save=False)

            # save the image object
            super(Article, self).save(force_update, force_insert)
        else:
            super(Article, self).save()


def has_changed(instance, field, manager='objects'):
    """Returns true if a field has changed in a model
    May be used in a model.save() method.
    """
    if not instance.pk:
        return True
    manager = getattr(instance.__class__, manager)
    old = getattr(manager.get(pk=instance.pk), field)
    return not getattr(instance, field) == old


def get_last_articles():
    return Article.objects.all()\
        .filter(is_visible=True)\
        .order_by('-pubdate')[:5]


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
