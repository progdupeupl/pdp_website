# coding: utf-8

from pdp.utils import render_template

from pdp.article.models import get_last_articles
from pdp.tutorial.models import get_last_tutorials
from pdp.forum.models import get_last_topics


def home(request):
    '''
    Display the home page with last articles, tutorials and topics added
    '''
    return render_template('pages/home.html', {
        'last_articles': get_last_articles(),
        'last_tutorials': get_last_tutorials(),
        'last_topics': get_last_topics(),
    })


def help_markdown(request):
    '''
    Display a page with a markdown helper, used for compatibility if the user's
    browser doesn't support AJAX page loading with jQuery
    '''
    return render_template('pages/help_markdown.html')


def help_markdown_ajax(request):
    '''
    View used with jQuery in order to display markdown helper on textarea
    fields which always contain markdown formatted text
    '''
    return render_template('pages/help_markdown_part.html')
