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

from django.http import HttpResponse

from pdp.utils import render_template

from pdp.article.models import get_last_articles
from pdp.tutorial.models import get_last_tutorials
from pdp.forum.models import get_last_topics


def home(request):
    """Display the home page with last articles, tutorials and topics added.

    Returns:
        HttpResponse

    """
    return render_template('home.html', {
        'last_articles': get_last_articles(),
        'last_tutorials': get_last_tutorials(),
        'last_topics': get_last_topics(),
    })


def index(request):
    """Display list of available static pages.

    Returns:
        HttpResponse

    """
    return render_template('pages/index.html')


def help_markdown(request):
    """Display a page with a markdown helper.

    Returns:
        HttpResponse

    """
    return render_template('pages/help_markdown.html')


def help_writting(request):
    """Display a page with help about tutorial writting."""
    return render_template('pages/help_writting.html')


def about(request):
    """Display many informations about the website.

    Returns:
        HttpResponse

    """
    return render_template('pages/about.html')


def robots(request):
    """Display robots.txt file.

    Returns:
        HttpResponse

    """
    with open('robots.txt') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/plain')
