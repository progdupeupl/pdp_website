# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

from django import forms


class TopicForm(forms.Form):
    title = forms.CharField(max_length=80)
    subtitle = forms.CharField(max_length=255, required=False)
    text = forms.CharField(widget=forms.Textarea)


class PostForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea)
