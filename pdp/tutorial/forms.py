# coding: utf-8

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field
from crispy_forms.bootstrap import FormActions


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
        required=False
    )

    icon = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Général',
                Field('title', css_class='input-xxlarge'),
                Field('description', css_class='input-block-level'),
                'is_mini'
            ),
            FormActions(
                Submit('submit', 'Valider')
            )
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
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Général',
                Field('title', css_class='input-xxlarge'),
                Field('description', css_class='input-block-level'),
            ),
            FormActions(
                Submit('submit', 'Valider')
            )
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
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'

        self.helper.layout = Layout(
            Fieldset(
                u'Général',
                Field('title', css_class='input-xxlarge')
            ),
            Fieldset(
                u'Contenu',
                Field('introduction', css_class='input-block-level'),
                Field('conclusion', css_class='input-block-level')
            ),
            FormActions(
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
            FormActions(
                Submit('submit', 'Valider')
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
            FormActions(
                Submit('submit', 'Valider')
            )
        )
        super(EmbdedChapterForm, self).__init__(*args, **kwargs)


class ExtractForm(forms.Form):
    title = forms.CharField(max_length=80)
    text = forms.CharField(widget=forms.Textarea)
