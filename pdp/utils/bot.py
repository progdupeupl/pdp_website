# coding: utf-8

from datetime import datetime

from pdp.forum.models import Topic, Post


def create_tutorial_topic(tutorial, bot_pk=1, forum_pk=1):
    '''Creates a new topic for a tutorial'''

    # TODO: Use settings.py for bot_pk and forum_pk vars

    md = u'**{}**  \n{}\n\n[» Voir le tutoriel]({})'\
        .format(tutorial.title,
                tutorial.description,
                tutorial.get_absolute_url())

    topic = Topic(
        title=u'[Tutoriel] {}'.format(tutorial.title),
        subtitle=tutorial.description,
        author_id=bot_pk,
        pubdate=datetime.now(),
        forum_id=forum_pk)
    topic.save()

    post = Post(
        topic=topic,
        text=md,
        pubdate=datetime.now(),
        position_in_topic=1,
        author_id=bot_pk)
    post.save()

    topic.last_message=post
    topic.save()
