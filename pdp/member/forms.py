# coding: utf-8

from django import forms

from django.contrib.auth.models import User

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Field, HTML
from crispy_forms.bootstrap import FormActions

from captcha.fields import CaptchaField

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=76, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.CharField(label='Adresse email')
    username = forms.CharField(label='Nom d\'utilisateur', max_length=30)
    password = forms.CharField(label='Mot de passe', max_length=76, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Confirmation', max_length=76, widget=forms.PasswordInput)
    captcha = CaptchaField()

    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'


        self.helper.layout = Layout(
            Fieldset(
                u'Identifiants',
                Field('username'),
                Field('password'),
                Field('password_confirm'),
                Field('email'),
            ),
            Fieldset(
                u'Captcha',
                Field('captcha'),
            ),
            FormActions(
                Submit('submit', 'Valider mon inscription'),
                HTML('<a href="/" class="btn">Annuler</a>'),
            )
        )
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()

        # Check that the password and it's confirmation match
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if not password_confirm == password:
            msg = u'Les mots de passe sont différents'
            self._errors['password'] = self.error_class([''])
            self._errors['password_confirm'] = self.error_class([msg])

            del cleaned_data['password']
            del cleaned_data['password_confirm']

        # Check that the user doesn't exist yet

        username = cleaned_data.get('username')
        if User.objects.filter(username=username).count() > 0:
            msg = u'Ce nom d\'utilisateur est déjà utilisé'
            self._errors['username'] = self.error_class([msg])

        return cleaned_data


class ProfileForm(forms.Form):
    biography = forms.CharField(required=False, widget=forms.Textarea)
    site = forms.CharField(required=False, max_length=128)
    show_email = forms.BooleanField(required=False)
