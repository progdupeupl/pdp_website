from pdp.utils import render_template

from pdp.article.models import get_last_articles
from pdp.tutorial.models import get_last_tutorials


def accueil(request):
    return render_template('accueil.html', {
        'last_articles': get_last_articles(),
        'last_tutorials': get_last_tutorials(),
    })
