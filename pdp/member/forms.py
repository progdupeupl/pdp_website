# coding: utf-8

from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=76, widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    email = forms.CharField()
    username = forms.CharField(max_length=30)
    password = forms.CharField(max_length=76, widget=forms.PasswordInput)
    show_email = forms.BooleanField(required=False)


class ProfileForm(forms.Form):
    biography = forms.CharField(required=False, widget=forms.Textarea)
    site = forms.CharField(required=False, max_length=128)
    show_email = forms.BooleanField(required=False)