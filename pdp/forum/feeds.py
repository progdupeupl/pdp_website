from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from .models import Post

from pdp.utils.templatetags.emarkdown import emarkdown


class LastPostsFeedRSS(Feed):
    title = "Posts sur Progdupeupl"
    link = "/forums/"
    description = "Les derniers messages parus sur le forum de Progdupeupl."

    def items(self):
        return Post.objects\
            .order_by('-pubdate')[:5]

    def item_title(self, item):
        return u'{}, message #{}'.format(item.topic.title, item.pk)

    def item_description(self, item):
        # TODO: Use cached Markdown when implemented
        return emarkdown(item.text)

    def item_author_name(self, item):
        return item.author.username

    def item_author_link(self, item):
        return item.author.get_absolute_url()

    def item_link(self, item):
        return item.get_absolute_url()


class LastPostsFeedATOM(LastPostsFeedRSS):
    feed_type = Atom1Feed
    subtitle = LastPostsFeedRSS.description
