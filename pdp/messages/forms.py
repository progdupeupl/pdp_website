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
from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Submit, Field, HTML


class PrivateTopicForm(forms.Form):
    recipients = forms.CharField(
        label=u'Participants (séparés par une virgule)',
        required=True)

    title = forms.CharField(
        label=u'Titre', required=True,
        max_length=80)

    subtitle = forms.CharField(
        label=u'Sous-titre',
        max_length=255, required=False)

    text = forms.CharField(
        label=u'Texte',
        widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('recipients'),
            Field('title'),
            Field('subtitle'),
            HTML('{% include "misc/editor.part.html" %}'),
            Field('text'),
            Submit('submit', u'Envoyer'),
            Submit('preview', u'Prévisualisation'),
        )
        super().__init__(*args, **kwargs)

    def clean_recipients(self):
        data = self.cleaned_data['recipients']

        bad_recipients = []
        for recipient in data.split(','):
            recipient = recipient.strip()

            try:
                User.objects.get(username=recipient)
            except User.DoesNotExist:
                bad_recipients.append(recipient)

        if bad_recipients:
            msg = u'Les utilisateurs suivants n’existent pas : {}.'.format(
                ', '.join(bad_recipients).strip()
            )
            self._errors['recipients'] = self.error_class([msg])

        return data


class PrivatePostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
