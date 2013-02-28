# coding: utf-8

from pdp.utils import render_template

from pdp.article.models import get_last_articles
from pdp.tutorial.models import get_last_tutorials


def home(request):
    return render_template('home.html', {
        'last_articles': get_last_articles(),
        'last_tutorials': get_last_tutorials(),
    })
