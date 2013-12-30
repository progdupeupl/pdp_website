# coding: utf-8

"""Models for article app."""

import os
import string
from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from taggit.managers import TaggableManager

from pdp.utils import slugify
from pdp.utils.models import has_changed

from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile

IMAGE_MAX_WIDTH = 64
IMAGE_MAX_HEIGHT = 64


def image_path(instance, filename):
    """Return path to an article image.

    Returns:
        string

    """
    ext = filename.split('.')[-1]
    filename = u'original.{}'.format(string.lower(ext))
    return os.path.join('articles', str(instance.pk), filename)


def thumbnail_path(instance, filename):
    """Return path to an article thumbnail.

    Returns:
        string

    """
    ext = filename.split('.')[-1]
    filename = u'thumb.{}'.format(string.lower(ext))
    return os.path.join('articles', str(instance.pk), filename)


class Article(models.Model):

    """An article."""

    class Meta:
        verbose_name = u'Article'
        verbose_name_plural = u'Articles'

    title = models.CharField(u'Titre', max_length=80)
    description = models.CharField(u'Description', max_length=200)

    text = models.TextField(u'Texte')

    author = models.ForeignKey(User, verbose_name=u'Auteur',
                               related_name='articles')

    slug = models.SlugField(max_length=80)

    pubdate = models.DateTimeField(u'Date de publication', blank=True)

    tags = TaggableManager()

    image = models.ImageField(upload_to=image_path,
                              blank=True, null=True, default=None)
    thumbnail = models.ImageField(upload_to=thumbnail_path,
                                  blank=True, null=True, default=None)

    is_visible = models.BooleanField(u'Est visible publiquement')
    is_pending = models.BooleanField(u'Est en attente')
    is_beta = models.BooleanField(u'Est visible par les membres',
                                  default=False)

    def __unicode__(self):
        """Textual representation of an article.

        Returns:
            string

        """
        return self.title

    def get_absolute_url(self):
        """Get URL to view the article.

        Returns:
            string

        """
        return reverse('pdp.article.views.view', args=(
            self.pk, self.slug))

    def get_edit_url(self):
        """Get URL to edit the article.

        Returns:
            string

        """
        return '/articles/editer?article={0}'.format(self.pk)

    def get_download_url(self):
        return u'{}?article={}'.format(
            reverse('pdp.article.views.download'),
            self.pk)

    def save(self, force_update=False, force_insert=False,
             thumb_size=(IMAGE_MAX_HEIGHT, IMAGE_MAX_WIDTH)):
        """Save the article.

        This will save thumbnail on disk and then save the model in database.

        """
        self.slug = slugify(self.title)

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


def get_last_articles():
    """Get the last published articles.

    This should be used for the home page article displaying.

    Returns:
        list of Tutorial

    """
    return Article.objects.all()\
        .filter(is_visible=True)\
        .order_by('-pubdate')[:5]


def get_prev_article(g_article):
    """Try to get the previous article ordered by pubdate.

    If g_article is the first article ever, None will be returned.

    Returns:
        Article

    """
    try:
        return Article.objects\
            .filter(is_visible=True)\
            .filter(pubdate__lt=g_article.pubdate)\
            .order_by('-pubdate')[0]
    except IndexError:
        return None


def get_next_article(g_article):
    """Try to get the next article ordered by pubdate.

    If g_article is the last one, None will be returned.

    Returns:
        Article

    """
    try:
        return Article.objects\
            .filter(is_visible=True)\
            .filter(pubdate__gt=g_article.pubdate)\
            .order_by('pubdate')[0]
    except IndexError:
        return None
