# coding: utf-8

from django import forms

class ArticleForm(forms.Form):
    title = forms.CharField(max_length=80)
    description = forms.CharField(max_length=200)
    text = forms.CharField(widget=forms.Textarea)