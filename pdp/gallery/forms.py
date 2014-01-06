# coding: utf-8

"""Forms for gallery app."""

from django import forms
from django.conf import settings


class UserGalleryForm(forms.Form):
    user = forms.CharField(label=u'Membre', required=False)
    gallery = forms.CharField(label=u'Gallerie', required=False)
    mode = forms.CharField(label=u'Mode', required=False)


class GalleryForm(forms.Form):
    title = forms.CharField(max_length=80)
    subtitle = forms.CharField(max_length=200, required=False)


class ImageForm(forms.Form):
    gallery = forms.CharField(label=u'Gallery', required=False)

    physical = forms.ImageField(
        label='Select an image',
        help_text=u'max. {} megabytes'.format(settings.IMAGE_MAX_SIZE),
        required=False)

    title = forms.CharField(label=u'Titre')
    legend = forms.CharField(label=u'Légende', required=False)
