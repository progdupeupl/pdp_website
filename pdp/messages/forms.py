# coding: utf-8

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Submit, Field, HTML


class PrivateTopicForm(forms.Form):
    participants = forms.CharField(
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
            Field('participants'),
            Field('title'),
            Field('subtitle'),
            HTML('{% include "misc/editor.part.html" %}'),
            Field('text'),
            Submit('submit', u'Envoyer'),
            Submit('preview', u'Prévisualisation'),
        )
        super(PrivateTopicForm, self).__init__(*args, **kwargs)


class PrivatePostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
