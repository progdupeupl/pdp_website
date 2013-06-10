# coding: utf-8

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, Div

from crispy_forms_foundation.layout import Layout, Fieldset, Submit, Field, ButtonHolder


class TutorialForm(forms.Form):
    title = forms.CharField(
        label='Titre',
        max_length=80
    )

    description = forms.CharField(
        max_length=200
    )

    is_mini = forms.BooleanField(
        label='Mini-tutoriel',
        required=False,
        initial=True
    )

    icon = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            'is_mini',
            Submit('submit', 'Valider')
        )
        super(TutorialForm, self).__init__(*args, **kwargs)


class EditTutorialForm(forms.Form):
    title = forms.CharField(
        label='Titre',
        max_length=80
    )

    description = forms.CharField(
        max_length=200
    )

    icon = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('description'),
            Submit('submit', 'Valider')
        )
        super(EditTutorialForm, self).__init__(*args, **kwargs)


class PartForm(forms.Form):
    title = forms.CharField(
        label='Titre',
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

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Général',
                Field('title')
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
        super(PartForm, self).__init__(*args, **kwargs)


class ChapterForm(forms.Form):
    title = forms.CharField(
        label='Titre',
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

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Général',
                Field('title', css_class='input-xxlarge'),
            ),
            Fieldset(
                u'Contenu',
                Field('introduction', css_class='input-block-level'),
                Field('conclusion', css_class='input-block-level')
            ),
            ButtonHolder(
                Div(
                    Submit('submit', 'Ajouter'),
                    Submit('submit_continue', 'Ajouter et continuer', css_class='secondary'),
                    css_class='button-group'
                ),
            )
        )
        super(ChapterForm, self).__init__(*args, **kwargs)


class EmbdedChapterForm(forms.Form):
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
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Contenu',
                Field('introduction', css_class='input-block-level'),
                Field('conclusion', css_class='input-block-level')
            ),
            ButtonHolder(
                Submit('submit', 'Valider')
            )
        )
        super(EmbdedChapterForm, self).__init__(*args, **kwargs)


class ExtractForm(forms.Form):
    title = forms.CharField(
        label='Titre',
        max_length=80
    )

    text = forms.CharField(
        label='Texte',
        required=False,
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('text'),
            Div(
                Submit('submit', 'Ajouter'),
                Submit('submit_continue', 'Ajouter et continuer', css_class='secondary'),
                css_class='button-group'
            )
        )
        super(ExtractForm, self).__init__(*args, **kwargs)
        

class EditExtractForm(forms.Form):
    title = forms.CharField(
        label='Titre',
        max_length=80
    )

    text = forms.CharField(
        label='Texte',
        required=False,
        widget=forms.Textarea
    )

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Field('title'),
            Field('text'),
            Submit('submit', 'Modifier'),
        )
        super(EditExtractForm, self).__init__(*args, **kwargs)