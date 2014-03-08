# coding: utf-8

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms_foundation.layout import Layout, Submit, Field, HTML

from pdp.article.models import ArticleCategory

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

    category = forms.ModelChoiceField(
        label=u'Catégorie',
        queryset=ArticleCategory.objects.all()
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            Field('image'),
            Field('tags'),
            Field('category'),
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
