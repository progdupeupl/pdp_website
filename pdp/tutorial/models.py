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

"""Models for tutorial app.

The class hierarchy is as follows :
 - "large" tutorials: Tutorial < Parts < Chapters < Extracts
 - "medium" tutorials: Tutorial < Part < Chapters < Extracts
 - "small" tutorials : Tutorial < Chapter < Extracts

"""
import os
import string

from django.db import models
from django.db.models.signals import post_save

from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth.models import User

from django.core.urlresolvers import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from taggit.managers import TaggableManager

from PIL import Image
from cStringIO import StringIO

from pdp.tutorial.exceptions import \
    OrphanPartException, OrphanChapterException

from pdp.utils import slugify
from pdp.utils.models import has_changed

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


class TutorialCategory(models.Model):

    """A way to organize tutorials in different categories."""

    class Meta:
        verbose_name = u'Catégorie de tutoriel'
        verbose_name_plural = u'Catégories de tutoriel'

    title = models.CharField(u'Titre', max_length=80)
    slug = models.SlugField(max_length=80)

    def __unicode__(self):
        """Textual representation of a category."""
        return self.title

    def get_absolute_url(self):
        """Get URL to view the category."""
        return reverse('pdp.tutorial.views.by_category', args=(
            self.slug,
        ))

    def get_tutorial_count(self):
        """Return number of visible tutorials in this category."""
        return Tutorial.objects \
            .filter(is_visible=True) \
            .filter(category__pk=self.pk) \
            .count()


class Tutorial(models.Model):

    """A tutorial, large or small."""

    class Meta:
        verbose_name = u'Tutoriel'
        verbose_name_plural = u'Tutoriels'

    SMALL = 'S'
    MEDIUM = 'M'
    BIG = 'B'

    SIZE_CHOICES = (
        (SMALL, u'Mini'),
        (MEDIUM, u'Standard'),
        (BIG, u'Étendu'),
    )

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
    # than a field.
    size = models.CharField(u'Taille du tutoriel', max_length=1,
                            choices=SIZE_CHOICES, default=BIG)

    is_visible = models.BooleanField(u'Est visible publiquement',
                                     default=False)
    is_pending = models.BooleanField(u'Est en attente', default=False)
    is_beta = models.BooleanField(u'Est en bêta', default=False)

    category = models.ForeignKey(TutorialCategory, null=True, blank=True,
                                 verbose_name=u'Catégorie')

    tags = TaggableManager()

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

    def get_pdf_url(self):
        """Get URL to get a PDF file of this tutorial."""
        return u'{}/tutorials/{}/{}.pdf'.format(
            settings.MEDIA_URL,
            self.pk,
            self.slug,
        )

    def get_md_url(self):
        """Get URL to get a MD file of this tutorial."""
        return u'{}/tutorials/{}/{}.md'.format(
            settings.MEDIA_URL,
            self.pk,
            self.slug,
        )

    def has_pdf(self):
        """Check if the tutorial has a PDF file."""
        return os.path.isfile(os.path.join(
            settings.MEDIA_ROOT,
            'tutorials',
            str(self.pk),
            u'{}.pdf'.format(self.slug),
        ))

    def has_md(self):
        """Check if the tutorial has a markdown file"""
        return os.path.isfile(os.path.join(
            settings.MEDIA_ROOT,
            'tutorials',
            str(self.pk),
            u'{}.md'.format(self.slug),
        ))

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

    def get_part(self):
        """Get the part associated with the tutorial if medium."""
        return self.get_parts().first()

    def get_chapter(self):
        """Get the chapter associated with the tutorial if it's small.

        Returns:
            Chapter

        Raises:
            CorruptedTutorialError

        """
        if not self.size == Tutorial.SMALL:
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
    position_in_tutorial = models.IntegerField(u'Position dans le tutoriel',
                                               null=True, blank=True)

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
        if self.tutorial.size == "B":
            return reverse('pdp.tutorial.views.view_part', args=[
                self.tutorial.pk,
                self.tutorial.slug,
                self.slug,
            ])
        else:
            return reverse('pdp.tutorial.views.view_tutorial', args=[
                self.tutorial.pk,
                self.tutorial.slug,
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
            # Whoops, this chapter is orphan, but better return a fake URL than
            # raise an exception here.
            return reverse('pdp.tutorial.views.index')

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

        Raises:
            OrphanPartException, OrphanChapterException

        """
        if self.part:
            if self.part.tutorial:
                return self.part.tutorial
            else:
                raise OrphanPartException
        elif self.tutorial:
            return self.tutorial
        else:
            raise OrphanChapterException

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


@receiver(post_save, sender=Tutorial)
def saved_tutorial_handler(sender, **kwargs):
    """Function called on each tutorial save."""
    if not settings.TESTING:
        from pdp.utils.tutorials import export_tutorial_pdf
        export_tutorial_pdf(kwargs.get('instance', None))


@receiver(post_save, sender=Part)
def saved_part_handler(sender, **kwargs):
    """Function called on each tutorial save."""
    if not settings.TESTING:
        from pdp.utils.tutorials import export_tutorial_pdf
        export_tutorial_pdf(kwargs.get('instance', None).tutorial)


@receiver(post_save, sender=Chapter)
def saved_chapter_handler(sender, **kwargs):
    """Function called on each tutorial save."""
    if not settings.DEBUG:
        from pdp.utils.tutorials import export_tutorial_pdf
        export_tutorial_pdf(kwargs.get('instance', None).get_tutorial())


@receiver(post_save, sender=Extract)
def saved_extract_handler(sender, **kwargs):
    """Function called on each tutorial save."""
    if not settings.TESTING:
        from pdp.utils.tutorials import export_tutorial_pdf
        export_tutorial_pdf(
            kwargs.get('instance', None).chapter.get_tutorial()
        )
