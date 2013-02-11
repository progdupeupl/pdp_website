from django import forms
from models import Profile

from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=76, widget=forms.PasswordInput)

class ProfileForm(forms.Form):
    biography = forms.CharField(required=False, widget=forms.Textarea)
    show_email = forms.BooleanField(required=False)
