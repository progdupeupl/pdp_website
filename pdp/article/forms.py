# coding: utf-8

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Submit, Field


class ArticleForm(forms.Form):
    title = forms.CharField(
        label='Titre',
        max_length=80
    )

    description = forms.CharField(
        max_length=200
    )

    text = forms.CharField(
        label='Texte',
        required=False,
        widget=forms.Textarea
    )

    tags = forms.CharField(
        label='Tags',
        max_length=80,
        required=False
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title', css_class='input-xxlarge'),
            Field('description', css_class='input-block-level'),
            Field('text', css_class='input-block-level'),
            Field('tags'),
            Submit('submit', 'Valider'),
        )
        super(ArticleForm, self).__init__(*args, **kwargs)
