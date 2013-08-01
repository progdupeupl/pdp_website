from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Tutorial


class LastTutorialsFeedRSS(Feed):
    title = "Tutoriels sur Progdupeupl"
    link = "/tutoriels/"
    description = "Les derniers tutoriels parus sur Progdupeupl."

    def items(self):
        return Tutorial.objects\
            .filter(is_visible=True)\
            .order_by('-pubdate')[:5]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.description

    def item_author_name(self, item):
        return ', '.join([author.username for author in item.authors.all()])

    def item_link(self, item):
        return item.get_absolute_url()


class LastTutorialsFeedATOM(LastTutorialsFeedRSS):
    feed_type = Atom1Feed
    subtitle = LastTutorialsFeedRSS.description
