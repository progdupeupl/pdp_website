# coding: utf-8

from pdp.utils import render_template

from pdp.article.models import get_last_articles
from pdp.tutorial.models import get_last_tutorials
from pdp.forum.models import get_last_topics


def home(request):
    return render_template('pages/home.html', {
        'last_articles': get_last_articles(),
        'last_tutorials': get_last_tutorials(),
        'last_topics': get_last_topics(),
    })


def help_markdown(request):
    return render_template('pages/help_markdown.html')


def help_markdown_ajax(request):
    return render_template('pages/help_markdown_part.html')
