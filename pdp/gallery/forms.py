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

"""Forms for gallery app."""

from django import forms
from django.conf import settings

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Field, Submit, HTML


class UserGalleryForm(forms.Form):
    user = forms.CharField(label=u'Membre', required=False)
    gallery = forms.CharField(label=u'Gallerie', required=False)
    mode = forms.CharField(label=u'Mode', required=False)


class GalleryForm(forms.Form):
    title = forms.CharField(
        label=u'Titre',
        max_length=80)

    subtitle = forms.CharField(
        label=u'Sous-titre',
        max_length=200,
        required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('subtitle'),
            Submit('submit', u'Créer la galerie'),
            HTML(u'<a href="{% url "pdp.gallery.views.gallery_list" %}" '
                 u'class="button secondary">Retour</a>')
        )
        super().__init__(*args, **kwargs)


class ImageForm(forms.Form):
    gallery = forms.CharField(
        label=u'Gallery',
        required=False)

    physical = forms.ImageField(
        label=u'Image (max. {} ko)'.format(settings.IMAGE_MAX_SIZE / 1024))

    title = forms.CharField(
        label=u'Titre')

    legend = forms.CharField(
        label=u'Légende',
        required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('legend'),
            Field('physical'),
            Submit('submit', u'Ajouter l’image'),
            HTML(u'<a href="{{ gallery.get_absolute_url }}" '
                 u'class="button secondary">Annuler</a>')
        )
        super().__init__(*args, **kwargs)


class EditImageForm(forms.Form):
    gallery = forms.CharField(
        label=u'Gallery',
        required=False)

    title = forms.CharField(
        label=u'Titre')

    legend = forms.CharField(
        label=u'Légende',
        required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('legend'),
            Submit('submit', u'Modifier'),
            HTML(u'<a href="{{ gallery.get_absolute_url }}" '
                 u'class="button secondary">Retour</a>')
        )
        super().__init__(*args, **kwargs)
