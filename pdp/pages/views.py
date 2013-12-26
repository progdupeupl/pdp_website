# coding: utf-8

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


def about(request):
    """Display many informations about the website.

    Returns:
        HttpResponse

    """
    return render_template('pages/about.html')
