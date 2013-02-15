# coding: utf-8

from django import forms


class TutorialForm(forms.Form):
    title = forms.CharField(max_length=80)
    description = forms.CharField(max_length=200)
    is_mini = forms.BooleanField(required=False)
    icon = forms.ImageField(required=False)


class PartForm(forms.Form):
    title = forms.CharField(max_length=80)
    introduction = forms.CharField(widget=forms.Textarea)
    conclusion = forms.CharField(widget=forms.Textarea)


class ChapterForm(forms.Form):
    title = forms.CharField(max_length=80)
    description = forms.CharField(max_length=200, required=False)
    introduction = forms.CharField(widget=forms.Textarea)
    conclusion = forms.CharField(widget=forms.Textarea)


class ExtractForm(forms.Form):
    title = forms.CharField(max_length=80)
    text = forms.CharField(widget=forms.Textarea)
