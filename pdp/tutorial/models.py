# coding: utf-8

"""Tutorial app's database models and model-related functions.

The class hierarchy is as follows :
 - "large" tutorials: Tutorial < Parts < Chapters
 - "small" tutorials : Tutorial < Chapter

"""
import os
import string

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from pdp.utils import slugify
from pdp.utils.models import has_changed

from PIL import Image
from cStringIO import StringIO
from django.core.files.uploadedfile import SimpleUploadedFile

IMAGE_MAX_WIDTH = 64
IMAGE_MAX_HEIGHT = 64


def image_path(instance, filename):
    """Get path to a tutorial image.

    Returns:
        string

    """
    ext = filename.split('.')[-1]
    filename = u'original.{}'.format(string.lower(ext))
    return os.path.join('tutorials', str(instance.pk), filename)


def thumbnail_path(instance, filename):
    """Get path to a tutorial thumbnail.

    Returns:
        string

    """
    ext = filename.split('.')[-1]
    filename = u'thumb.{}'.format(string.lower(ext))
    return os.path.join('tutorials', str(instance.pk), filename)


class Tutorial(models.Model):

    """A tutorial, large or small."""

    class Meta:
        verbose_name = u'Tutoriel'
        verbose_name_plural = u'Tutoriels'

    title = models.CharField(u'Titre', max_length=80)
    description = models.CharField(u'Description', max_length=200)
    authors = models.ManyToManyField(User, verbose_name=u'Auteurs')

    image = models.ImageField(upload_to=image_path,
                              blank=True, null=True, default=None)
    thumbnail = models.ImageField(upload_to=thumbnail_path,
                                  blank=True, null=True, default=None)

    introduction = models.TextField(u'Introduction', null=True, blank=True)
    conclusion = models.TextField(u'Conclusion', null=True, blank=True)

    slug = models.SlugField(max_length=80)

    pubdate = models.DateTimeField(u'Date de publication', blank=True)

    # We could distinguish large/small tutorials by looking at what chapters
    # are contained directly in a tutorial, but that'd be more complicated
    # than a field
    is_mini = models.BooleanField(u'Est un mini-tutoriel')

    is_visible = models.BooleanField(u'Est visible publiquement')
    is_pending = models.BooleanField(u'Est en attente', default=False)
    is_beta = models.BooleanField(u'Est en bêta', default=False)

    def __unicode__(self):
        """Textual representation of a tutorial.

        Returns:
            string

        """
        return self.title

    def get_absolute_url(self):
        """Get URL to view this tutorial.

        Returns:
            string

        """
        return reverse('pdp.tutorial.views.view_tutorial', args=[
            self.pk, slugify(self.title)
        ])

    def get_edit_url(self):
        """Get URL to edit this tutorial.

        Returns:
            string

        """
        return u'/tutoriel/editer?tutoriel={0}'.format(self.pk)

    def get_parts(self):
        """Get the parts associated with the tutorial if it's big.

        Returns:
            list of Part

        """
        return Part.objects.all()\
            .filter(tutorial__pk=self.pk)\
            .order_by('position_in_tutorial')

    def get_chapter(self):
        """Get the chapter associated with the tutorial if it's small.

        Returns:
            Chapter

        """
        if not self.is_mini:
            return None

        try:
            # We can use get since we know there'll only be one chapter
            return Chapter.objects.get(tutorial__pk=self.pk)
        except Chapter.DoesNotExist:
            # Whoops, this tutorial is broken!
            return None

    def save(self, force_update=False, force_insert=False,
             thumb_size=(IMAGE_MAX_HEIGHT, IMAGE_MAX_WIDTH)):
        """Save tutorial instance.

        If tutorial's image was changed, it will update its thumbnail field
        resizing it. Then it will call normal saving of the model.

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
            self.thumbnail.save(u'{}.png'.format(suf.name), suf, save=False)

            # save the image object
            super(Tutorial, self).save(force_update, force_insert)
        else:
            super(Tutorial, self).save()


def get_last_tutorials():
    """Get the last published tutorials.

    This should be used for the home page tutorial displaying.

    Returns:
        list of Tutorial

    """
    return Tutorial.objects.all() \
        .filter(is_visible=True) \
        .order_by('-pubdate')[:5]


class Part(models.Model):

    """A part, containing chapters."""

    class Meta:
        verbose_name = u'Partie'
        verbose_name_plural = u'Parties'

    # A part has to belong to a tutorial, since only tutorials with parts
    # are large tutorials
    tutorial = models.ForeignKey(Tutorial, verbose_name=u'Tutoriel parent')
    position_in_tutorial = models.IntegerField(u'Position dans le tutoriel')

    title = models.CharField(u'Titre', max_length=80)

    introduction = models.TextField(u'Introduction')
    conclusion = models.TextField(u'Conclusion')

    slug = models.SlugField(max_length=80)

    # The list of chapters is shown between introduction and conclusion

    def save(self, *args, **kwargs):
        """Save a part.

        This will compute the slug field from title field and then save the
        model.

        """
        self.slug = slugify(self.title)
        super(Part, self).save(*args, **kwargs)

    def __unicode__(self):
        """Textual representation of a part.

        Returns:
            string

        """
        return u'<Partie pour {0}, {1}>'\
            .format(self.tutorial.title, self.position_in_tutorial)

    def get_absolute_url(self):
        """Get URL to view the part.

        Returns:
            string

        """
        return reverse('pdp.tutorial.views.view_part', args=[
            self.tutorial.pk,
            self.tutorial.slug,
            self.slug,
        ])

    def get_chapters(self):
        """Get all the chapters of the part.

        Returns:
            Chapter list

        """
        return Chapter.objects.all()\
            .filter(part=self).order_by('position_in_part')


class Chapter(models.Model):

    """A chapter, containing some extracts."""

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
        """Textual representation on a chapter.

        Returns:
            string

        """
        if self.tutorial:
            return u'<minituto \'{0}\'>'.format(self.tutorial.title)
        elif self.part:
            return u'<bigtuto \'{0}\', \'{1}\'>'\
                .format(self.part.tutorial.title, self.title)
        else:
            return u'<orphelin>'

    def get_absolute_url(self):
        """Get URL to view this chapter.

        Returns:
            string

        """
        if self.tutorial:
            return self.tutorial.get_absolute_url()

        elif self.part:
            return self.part.get_absolute_url() + u'{0}/'.format(self.slug)

        else:
            return u'/tutoriels/'

    def get_extract_count(self):
        """Get the number of extracts in the chapter.

        Returns:
            int

        """
        return Extract.objects.all().filter(chapter__pk=self.pk).count()

    def get_extracts(self):
        """Get all the extracts of this chapter.

        Returns:
            Extract list

        """
        return Extract.objects.all()\
            .filter(chapter__pk=self.pk)\
            .order_by('position_in_chapter')

    def get_tutorial(self):
        """Get the tutorial owning this chapter.

        Returns:
            Tutorial

        """
        if self.part:
            return self.part.tutorial
        return self.tutorial

    def update_position_in_tutorial(self):
        """Update the position of the chapter.

        Update the position_in_tutorial field, but don't save it ; you have
        to call save() method manually if you want to save the new computed
        position.

        """
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
        """Save the chapter.

        This will update the chapter's thumbnail if its image was changed and
        then save the model.

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
            super(Chapter, self).save(force_update, force_insert)
        else:
            super(Chapter, self).save()


class Extract(models.Model):

    """A content extract from a chapter."""

    class Meta:
        verbose_name = u'Extrait'
        verbose_name_plural = u'Extraits'

    title = models.CharField(u'Titre', max_length=80)
    chapter = models.ForeignKey(Chapter, verbose_name=u'Chapitre parent')
    position_in_chapter = models.IntegerField(u'Position dans le chapitre')
    text = models.TextField(u'Texte')

    def __unicode__(self):
        """Textual representation of an extract.

        Returns:
            string

        """
        return u'<extrait \'{0}\'>'.format(self.title)

    def get_absolute_url(self):
        """Get the URL to view this extract.

        Returns:
            string

        """
        return u'{0}#{1}-{2}'.format(
            self.chapter.get_absolute_url(),
            self.position_in_chapter,
            slugify(self.title)
        )
