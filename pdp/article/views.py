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

from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse

from pdp.article.models import Article


def redirect_index(request):
    """Redirects to the tutorial index.

    Returns:
        HttpResponse

    """
    return redirect(reverse('pdp.tutorial.views.index'), permanent=True)


def redirect_view(request, article_pk, article_slug):
    """Redirects article to its equivalent tutorial.

    Returns:
        HttpResponse

    """
    article = get_object_or_404(Article, pk=article_pk)

    tutorial = article.to_tutorial
    if tutorial:
        return redirect(tutorial.get_absolute_url(), permanent=True)

    return redirect(reverse('pdp.tutorial.views.index'))


def redirect_feed_rss(request):
    """Redirect the article RSS feed to the tutorial feed.

    Returns:
        HttpResponse

    """
    return redirect('/tutoriels/flux/rss/', permanent=True)


def redirect_feed_atom(request):
    """Redirect the article ATOM feed to the tutorial feed.

    Returns:
        HttpResponse

    """
    return redirect('/tutoriels/flux/atom/', permanent=True)
