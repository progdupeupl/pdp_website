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

import os
import uuid

from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.urlresolvers import reverse


def image_path(instance, filename):
    """Return path to an image.

    Returns:
        string

    """
    ext = filename.split('.')[-1]
    filename = u'{}.{}'.format(str(uuid.uuid4()), ext.lower())
    return os.path.join('galleries', str(instance.gallery.pk), filename)


class UserGallery(models.Model):

    """Rights for an user on a specific gallery."""

    class Meta:
        verbose_name = "Galeries de l'utilisateur"
        verbose_name_plural = "Galeries de l'utilisateur"

    user = models.ForeignKey(User, verbose_name=(u'Membre'))
    gallery = models.ForeignKey('Gallery', verbose_name=(u'Galerie'))
    MODE_CHOICES = (
        ('R', 'Lecture'),
        ('W', 'Ecriture')
    )
    mode = models.CharField(max_length=1, choices=MODE_CHOICES, default='R')

    def __str__(self):
        """Textual form of an user gallery.

        Returns:
            string

        """
        return u'Galerie "{0}" envoye par {1}'.format(self.gallery,
                                                      self.user)

    def is_write(self):
        """Check if the user can add/edit images in the gallery.

        Returns:
            bool

        """
        return self.mode == 'W'

    def is_read(self):
        """Check if the user can see the gallery.

        Returns:
            bool

        """
        return self.mode == 'R'

    def get_images(self):
        """Get all the images of the remote gallery.

        Returns:
            Image list

        """
        return Image.objects.all()\
            .filter(gallery=self.gallery)\
            .order_by('update')

    def get_gallery(self, user):
        """Get the remote gallery.

        Returns:
            Gallery

        """
        # TODO: remove this func and just use obj.gallery instead of
        # obj.get_gallery.
        return self.gallery


class Image(models.Model):

    """Uploaded user image."""

    class Meta:
        verbose_name = "Image"
        verbose_name_plural = "Images"

    gallery = models.ForeignKey('Gallery', verbose_name=('Galerie'))
    title = models.CharField('Titre', max_length=80)
    slug = models.SlugField(max_length=80)
    physical = models.ImageField(upload_to=image_path)
    legend = models.CharField('Légende', max_length=80)
    pubdate = models.DateTimeField('Date de création', auto_now_add=True)
    update = models.DateTimeField(
        'Date de modification', null=True, blank=True)

    def __str__(self):
        """Textual representation of an Image.

        Returns:
            string

        """
        return self.title

    def get_absolute_url(self):
        """Get the URL of the image to be displayed.

        Returns:
            string

        """
        return '{0}/{1}'.format(settings.MEDIA_URL, self.physical)


# These two auto-delete files from filesystem when they are unneeded:

@receiver(models.signals.post_delete, sender=Image)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """Delete image from filesystem when corresponding object is deleted."""
    if instance.physical:
        if os.path.isfile(instance.physical.path):
            os.remove(instance.physical.path)


class Gallery(models.Model):

    """Gallery containing some Image instances."""

    class Meta:
        verbose_name = "Galerie"
        verbose_name_plural = "Galeries"

    title = models.CharField('Titre', max_length=80)
    subtitle = models.CharField('Sous titre', max_length=200, blank=True)
    slug = models.SlugField(max_length=80)
    pubdate = models.DateTimeField('Date de création', auto_now_add=True)
    update = models.DateTimeField(
        'Date de modification', null=True, blank=True)

    def __str__(self):
        """Textual form of an Gallery.

        Returns:
            string

        """
        return self.title

    def get_absolute_url(self):
        """Get URL to view this gallery.

        Returns:
            string

        """
        return reverse('pdp.gallery.views.gallery_details',
                       args=[self.pk, self.slug])

    def get_users(self):
        """Get all the user rights for this gallery.

        Returns:
            UserGallery list

        """
        return UserGallery.objects.all()\
            .filter(gallery=self)

    def get_real_users(self):
        """Get all the user for this gallery.

        Returns:
            User list

        """
        usrs = []
        for ug in self.get_users():
            usrs.append(ug.user)

        return usrs

    def get_images(self):
        """Get all the images published in the gallery.

        Returns:
            Image list

        """
        return Image.objects.all()\
            .filter(gallery=self)\
            .order_by('pubdate')

    def get_last_image(self):
        """Get the last image published in the gallery.

        Returns:
            Image or None

        """
        try:
            return Image.objects.all()\
                .filter(gallery=self)\
                .order_by('-pubdate')[0]
        except IndexError:
            return None
