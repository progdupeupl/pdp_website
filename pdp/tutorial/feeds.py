from django.core.cache import cache

from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Tutorial


class LastTutorialsFeedRSS(Feed):
    title = "Tutoriels sur Progdupeupl"
    link = "/tutoriels/"
    description = "Les derniers tutoriels parus sur Progdupeupl."

    def items(self):
        tutorials = cache.get('latest_tutorials')

        if tutorials is None:
            tutorial = Tutorial.objects\
                .filter(is_visible=True)\
                .order_by('-pubdate')[:5]

            cache.set('latest_tutorials', tutorials)

        return tutorials

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
