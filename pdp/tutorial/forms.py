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

from crispy_forms_foundation.layout import Layout, Fieldset, Submit, Field, \
    ButtonHolder, HTML

from pdp.tutorial.models import TutorialCategory, Tutorial, Part, Chapter
from pdp.utils import slugify


class TutorialForm(forms.Form):
    """Form used to create a new tutorial."""

    title = forms.CharField(
        label=u'Titre',
        max_length=80
    )

    image = forms.ImageField(
        label=u'Selectionnez une image',
        required=False)

    description = forms.CharField(
        max_length=200
    )

    tags = forms.CharField(
        label=u'Tags (séparés par une virgule)',
        max_length=80,
        required=False
    )

    category = forms.ModelChoiceField(
        label=u'Catégorie',
        queryset=TutorialCategory.objects.all(),
        required=False
    )

    size = forms.ChoiceField(
        label=u'Taille du tutoriel',
        choices=Tutorial.SIZE_CHOICES
    )

    icon = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            Field('tags'),
            Field('category'),
            Field('image'),
            Field('size'),
            Submit('submit', u'Créer')
        )
        super().__init__(*args, **kwargs)


class ImportTutorialForm(forms.Form):
    """Form used to import a tutorial from a MD file."""

    markdown = forms.FileField(
        label=u'Fichier markdown',
        required=True
    )

    size = forms.ChoiceField(
        label=u'Taille du tutoriel',
        choices=Tutorial.SIZE_CHOICES
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('markdown'),
            Field('size'),
            Submit('submit', u'Importer')
        )
        super().__init__(*args, **kwargs)


class EditTutorialForm(forms.Form):
    """Form used to edit an existing tutorial."""

    title = forms.CharField(
        label=u'Titre',
        max_length=80
    )

    description = forms.CharField(
        max_length=200
    )

    image = forms.ImageField(
        label=u'Selectionnez une image',
        required=False
    )

    tags = forms.CharField(
        label=u'Tags (séparés par une virgule)',
        max_length=80,
        required=False
    )

    category = forms.ModelChoiceField(
        label=u'Catégorie',
        queryset=TutorialCategory.objects.all(),
        required=False
    )

    introduction = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    conclusion = forms.CharField(
        required=False,
        widget=forms.Textarea
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
            Field('introduction'),
            Field('conclusion'),
            Submit('submit', 'Valider')
        )
        super().__init__(*args, **kwargs)


class AddPartForm(forms.Form):
    """Form used to add a part to a tutorial."""

    title = forms.CharField(
        label=u'Titre',
        max_length=80
    )

    introduction = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    conclusion = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    tutorial = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Général',
                Field('title'),
                Field('tutorial'),
            ),
            Fieldset(
                u'Contenu',
                Field('introduction'),
                Field('conclusion')
            ),
            ButtonHolder(
                Submit('submit', 'Valider'),
            )
        )
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        title = slugify(cleaned_data.get('title'))

        existing = [x.slug for x in Part.objects.all().filter(
            tutorial=Tutorial.objects.get(pk=cleaned_data.get('tutorial')))]

        if title in existing:
            msg = u'Une partie portant ce nom existe déjà dans ce tutoriel.'
            self.add_error('title', msg)

        return cleaned_data


class EditPartForm(forms.Form):
    """Form used to edit an existing part."""

    title = forms.CharField(
        label=u'Titre',
        max_length=80
    )

    introduction = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    conclusion = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    tutorial = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput
    )

    part = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Général',
                Field('title'),
                Field('tutorial'),
                Field('part')
            ),
            Fieldset(
                u'Contenu',
                Field('introduction'),
                Field('conclusion')
            ),
            ButtonHolder(
                Submit('submit', u'Sauvegarder les modifications'),
            )
        )
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        title = slugify(cleaned_data.get('title'))
        part = cleaned_data.get('part')

        existing = [x.slug for x in Part.objects.all()
                    .filter(tutorial=Tutorial.objects.get(
                        pk=cleaned_data.get('tutorial')))
                    .exclude(pk=part)]

        if title in existing:
            msg = u'Une partie portant ce nom existe déjà dans ce tutoriel.'
            self.add_error('title', msg)

        return cleaned_data


class AddChapterForm(forms.Form):
    """Form used to add a chapter to a part."""

    title = forms.CharField(
        label=u'Titre',
        max_length=80
    )

    introduction = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    image = forms.ImageField(
        label=u'Image',
        required=False)

    conclusion = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    part = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Général',
                Field('title'),
                Field('image'),
                Field('part'),
            ),
            Fieldset(
                u'Contenu',
                Field('introduction'),
                Field('conclusion'),
            ),
            ButtonHolder(
                Div(
                    Submit('submit', 'Ajouter'),
                    Submit(
                        'submit_continue', 'Ajouter et continuer',
                        css_class='secondary'),
                    css_class='button-group'
                ),
            )
        )
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        title = slugify(cleaned_data.get('title'))

        existing_chapters_titles = [x.slug for x in Chapter.objects.all()
                                    .filter(part=Part.objects.get(
                                        pk=cleaned_data.get('part')))]

        if title in existing_chapters_titles:
            msg = u'Un chapitre portant ce nom existe déjà dans cette partie.'
            self.add_error('title', msg)

        return cleaned_data


class EditChapterForm(forms.Form):
    """Form used to edit an existing chapter."""

    title = forms.CharField(
        label=u'Titre',
        max_length=80
    )

    introduction = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    image = forms.ImageField(
        label=u'Image',
        required=False)

    conclusion = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    part = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput
    )

    chapter = forms.IntegerField(
        required=True,
        widget=forms.HiddenInput
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Général',
                Field('title'),
                Field('image'),
                Field('part'),
                Field('chapter'),
            ),
            Fieldset(
                u'Contenu',
                Field('introduction'),
                Field('conclusion'),
            ),
            ButtonHolder(
                Submit('submit', u'Sauvegarder les modifications'),
            )
        )
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        title = slugify(cleaned_data.get('title'))
        chapter = cleaned_data.get('chapter')

        existing = [x.slug for x in Chapter.objects.all()
                    .filter(part=Part.objects.get(pk=cleaned_data.get('part')))
                    .exclude(pk=chapter)]

        if title in existing:
            msg = u'Un chapitre portant ce nom existe déjà dans cette partie.'
            self.add_error('title', msg)

        return cleaned_data


class EmbdedChapterForm(forms.Form):
    """Form used to edit a chapter for standalone chapters.

    This form may be used for small tutorials only.

    """

    introduction = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    image = forms.ImageField(
        label=u'Image',
        required=False)

    conclusion = forms.CharField(
        required=False,
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Contenu',
                Field('image'),
                Field('introduction'),
                Field('conclusion')
            ),
            ButtonHolder(
                Submit('submit', 'Valider')
            )
        )
        super().__init__(*args, **kwargs)


class ExtractForm(forms.Form):
    """Form used to add an extract to a chapter."""

    title = forms.CharField(
        label=u'Titre',
        max_length=80
    )

    text = forms.CharField(
        label=u'Texte',
        required=False,
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            HTML('{% include "misc/editor.part.html" %}'),
            Field('text'),
            Div(
                Submit('submit', u'Ajouter'),
                Submit('preview', u'Prévisualiser'),
                Submit(
                    'submit_continue', u'Ajouter et continuer',
                    css_class='secondary'),
                css_class='button-group'
            )
        )
        super().__init__(*args, **kwargs)


class EditExtractForm(forms.Form):
    """Form used to edit an existing extract."""

    title = forms.CharField(
        label=u'Titre',
        max_length=80
    )

    text = forms.CharField(
        label=u'Texte',
        required=False,
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            HTML('{% include "misc/editor.part.html" %}'),
            Field('text'),
            Submit('submit', u'Modifier'),
            Submit('preview', u'Prévisualiser')
        )
        super().__init__(*args, **kwargs)
