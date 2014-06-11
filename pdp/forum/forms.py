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

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Div

from crispy_forms_foundation.layout import Layout, Submit, HTML, Field


class TopicForm(forms.Form):
    title = forms.CharField(
        label=u'Titre',
        max_length=80,
        widget=forms.TextInput(attrs={'autofocus': 'autofocus'})
    )

    subtitle = forms.CharField(
        label=u'Sous-titre',
        max_length=255,
        required=False
    )

    text = forms.CharField(
        label=u'Texte',
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('subtitle',
                  placeholder=u'Facultatif, permet de mieux décrire votre '
                              u'sujet.'),
            HTML('{% include "misc/editor.part.html" %}'),
            Field('text',
                  placeholder=u'Contenu de votre message au format Markdown.'),
            Div(
                Submit('submit', u'Créer le sujet'),
                Submit('preview', u'Prévisualiser', css_class='secondary'),
                HTML(u'<a href="{{ forum.get_absolute_url }}" class="button '
                     u'secondary">Retour</a>'),
                css_class='button-center'
            )
        )
        super(TopicForm, self).__init__(*args, **kwargs)


class PostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
