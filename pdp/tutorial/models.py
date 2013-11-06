# coding: utf-8

from os import path
import os
import string

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from pdp.utils import slugify

from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile

# The class hierarchy is as follows :
# - "large" tutorials: Tutorial < Parts < Chapters
# - "small" tutorials : Tutorial < Chapter

IMAGE_MAX_WIDTH = 64
IMAGE_MAX_HEIGHT = 64


def image_path(instance, filename):
    '''Return path to an image'''
    ext = filename.split('.')[-1]
    filename = u'original.{}'.format(string.lower(ext))
    return os.path.join('tutorials', str(instance.pk), filename)


def thumbnail_path(instance, filename):
    '''Return path to an thumbnail'''
    ext = filename.split('.')[-1]
    filename = u'thumb.{}'.format(string.lower(ext))
    return os.path.join('tutorials', str(instance.pk), filename)


def tutorial_icon_path(instance, filename):
    return u'tutoriels/tutoriels/{0}{1}'\
        .format(instance.pk, path.splitext(filename)[1])


def part_icon_path(instance, filename):
    return u'tutoriels/parties/{0}{1}'\
        .format(instance.pk, path.splitext(filename)[1])


def chapter_icon_path(instance, filename):
    return 'tutoriels/chapitres/{0}{1}'\
        .format(instance.pk, path.splitext(filename)[1])


def has_changed(instance, field, manager='objects'):
    """Returns true if a field has changed in a model
    May be used in a model.save() method.
    """
    if not instance.pk:
        return True
    manager = getattr(instance.__class__, manager)
    old = getattr(manager.get(pk=instance.pk), field)
    return not getattr(instance, field) == old


class Tutorial(models.Model):
    '''A tutorial, large or small'''

    class Meta:
        verbose_name = 'Tutoriel'
        verbose_name_plural = 'Tutoriels'

    title = models.CharField('Titre', max_length=80)
    description = models.CharField('Description', max_length=200)
    authors = models.ManyToManyField(User, verbose_name='Auteurs')

    image = models.ImageField(upload_to=image_path,
                              blank=True, null=True, default=None)
    thumbnail = models.ImageField(upload_to=thumbnail_path,
                                  blank=True, null=True, default=None)

    introduction = models.TextField('Introduction', null=True, blank=True)
    conclusion = models.TextField('Conclusion', null=True, blank=True)

    slug = models.SlugField(max_length=80)

    pubdate = models.DateTimeField('Date de publication', blank=True)

    # We could distinguish large/small tutorials by looking at what chapters
    # are contained directly in a tutorial, but that'd be more complicated
    # than a field
    is_mini = models.BooleanField('Est un mini-tutoriel')

    is_visible = models.BooleanField('Est visible publiquement')
    is_pending = models.BooleanField('Est en attente', default=False)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pdp.tutorial.views.view_tutorial', args=[
            self.pk, slugify(self.title)
        ])

    def get_edit_url(self):
        return '/tutorial/editer?tutorial={0}'.format(self.pk)

    def get_parts(self):
        return Part.objects.all()\
            .filter(tutorial__pk=self.pk)\
            .order_by('position_in_tutorial')

    def get_chapter(self):
        '''Gets the chapter associated with the tutorial if it's small'''
        # We can use get since we know there'll only be one chapter
        return Chapter.objects.get(tutorial__pk=self.pk)

    def save(self, force_update=False, force_insert=False,
             thumb_size=(IMAGE_MAX_HEIGHT, IMAGE_MAX_WIDTH)):
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
            self.thumbnail.save(u'{}.png'.format(suf.name), suf, save=False)

            # save the image object
            super(Tutorial, self).save(force_update, force_insert)
        else:
            super(Tutorial, self).save()


def get_last_tutorials():
    return Tutorial.objects.all() \
        .filter(is_visible=True) \
        .order_by('-pubdate')[:5]


class Part(models.Model):

    '''A part, containing chapters'''
    class Meta:
        verbose_name = 'Partie'
        verbose_name_plural = 'Parties'

    # A part has to belong to a tutorial, since only tutorials with parts
    # are large tutorials
    tutorial = models.ForeignKey(Tutorial, verbose_name='Tutoriel parent')
    position_in_tutorial = models.IntegerField('Position dans le tutoriel')

    title = models.CharField('Titre', max_length=80)

    introduction = models.TextField('Introduction')
    conclusion = models.TextField('Conclusion')

    slug = models.SlugField(max_length=80)

    # The list of chapters is shown between introduction and conclusion

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Part, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'<Partie pour {0}, {1}>'\
            .format(self.tutorial.title, self.position_in_tutorial)

    def get_absolute_url(self):
        return reverse('pdp.tutorial.views.view_part', args=[
            self.tutorial.pk,
            self.tutorial.slug,
            self.slug,
        ])

    def get_chapters(self):
        return Chapter.objects.all()\
            .filter(part=self).order_by('position_in_part')


class Chapter(models.Model):

    '''A chapter, containing text'''
    class Meta:
        verbose_name = 'Chapitre'
        verbose_name_plural = 'Chapitres'

    # A chapter may belong to a part, that's where the difference between large
    # and small tutorials is.
    part = models.ForeignKey(Part, null=True, blank=True,
                             verbose_name='Partie parente')
    image = models.ImageField(upload_to=image_path, blank=True, null=True)
    thumbnail = models.ImageField(upload_to=image_path, blank=True, null=True)

    position_in_part = models.IntegerField('Position dans la partie',
                                           null=True, blank=True)

    # This field is required in order to use pagination in chapters, see the
    # update_position_in_tutorial() method.
    position_in_tutorial = models.IntegerField('Position dans le tutoriel',
                                               null=True, blank=True)

    # If the chapter doesn't belong to a part, it's a small tutorial; we need
    # to bind informations about said tutorial directly
    tutorial = models.ForeignKey(Tutorial, null=True, blank=True,
                                 verbose_name='Tutoriel parent')

    title = models.CharField('Titre', max_length=80, blank=True)

    introduction = models.TextField('Introduction')
    conclusion = models.TextField('Conclusion')

    slug = models.SlugField(max_length=80)

    def __unicode__(self):
        if self.tutorial:
            return u'<minituto \'{0}\'>'.format(self.tutorial.title)
        elif self.part:
            return u'<bigtuto \'{0}\', \'{1}\'>'\
                .format(self.part.tutorial.title, self.title)
        else:
            return u'<orphelin>'

    def get_absolute_url(self):
        if self.tutorial:
            return self.tutorial.get_absolute_url()

        elif self.part:
            return self.part.get_absolute_url() + '{0}/'.format(self.slug)

        else:
            return '/tutoriels/'

    def get_extract_count(self):
        return Extract.objects.all().filter(chapter__pk=self.pk).count()

    def get_extracts(self):
        return Extract.objects.all()\
            .filter(chapter__pk=self.pk)\
            .order_by('position_in_chapter')

    def get_tutorial(self):
        if self.part:
            return self.part.tutorial
        return self.tutorial

    def update_position_in_tutorial(self):
        '''
        Update the position_in_tutorial field, but don't save it ; you have
        to call save() method manually if you want to save the new computed
        position
        '''
        position = 1
        for part in self.part.tutorial.get_parts():
            if part.position_in_tutorial < self.part.position_in_tutorial:
                for chapter in part.get_chapters():
                    position += 1
            elif part == self.part:
                for chapter in part.get_chapters():
                    if chapter.position_in_part < self.position_in_part:
                        position += 1
        self.position_in_tutorial = position

    def save(self, force_update=False, force_insert=False,
             thumb_size=(IMAGE_MAX_HEIGHT, IMAGE_MAX_WIDTH)):
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
            super(Chapter, self).save(force_update, force_insert)
        else:
            super(Chapter, self).save()


class Extract(models.Model):

    '''A content extract from a chapter'''
    class Meta:
        verbose_name = 'Extrait'
        verbose_name_plural = 'Extraits'

    title = models.CharField('Titre', max_length=80)
    chapter = models.ForeignKey(Chapter, verbose_name='Chapitre parent')
    position_in_chapter = models.IntegerField('Position dans le chapitre')
    text = models.TextField('Texte')

    def __unicode__(self):
        return u'<extrait \'{0}\'>'.format(self.title)

    def get_absolute_url(self):
        return '{0}#{1}-{2}'.format(
            self.chapter.get_absolute_url(),
            self.position_in_chapter,
            slugify(self.title)
        )
