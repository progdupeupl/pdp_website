# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Submit, Field, HTML


class NewArticleForm(forms.Form):
    title = forms.CharField(
        label=u'Titre',
        max_length=80
    )

    description = forms.CharField(
        max_length=200
    )

    image = forms.ImageField(
        label=u'Icône',
        required=False)

    tags = forms.CharField(
        label=u'Tags (séparés par une virgule)',
        max_length=80,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            Field('image'),
            Field('tags'),
            Submit('submit', u'Créer l’article'),
        )
        super(NewArticleForm, self).__init__(*args, **kwargs)


class EditArticleForm(forms.Form):
    title = forms.CharField(
        label=u'Titre',
        max_length=80
    )

    description = forms.CharField(
        max_length=200
    )

    text = forms.CharField(
        label=u'Texte',
        required=False,
        widget=forms.Textarea
    )

    image = forms.ImageField(
        label=u'Icône',
        required=False)

    tags = forms.CharField(
        label=u'Tags (séparés par une virgule)',
        max_length=80,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            HTML('{% include "misc/editor.part.html" %}'),
            Field('text'),
            Field('image'),
            Field('tags'),
            Submit('submit', u'Enregistrer les modifications'),
        )
        super(EditArticleForm, self).__init__(*args, **kwargs)
