# coding: utf-8

"""Module used for interacting with the bot user, if any."""

from datetime import datetime

from django.template import Template, Context

from pdp.settings import BOT_USER_PK, BOT_TUTORIAL_FORUM_PK, \
    BOT_ARTICLE_FORUM_PK

from pdp.forum.models import Topic, Post


def create_topic(forum_pk, title, subtitle, text):
    """Create a new topic in a forum using the bot.

    Args:
        forum: forum instance identifier to post in
        title: title of the topic
        subtitle: subtitle of the topic, can be None
        text: content of the post in markdown

    """

    # Create topic
    topic = Topic(
        title=title,
        subtitle=subtitle,
        author_id=BOT_USER_PK,
        pubdate=datetime.now(),
        forum_id=forum_pk)

    # Save topic
    topic.save()

    # Create first post
    post = Post(
        topic=topic,
        text=text,
        pubdate=datetime.now(),
        position_in_topic=1,
        author_id=BOT_USER_PK)

    # Save post
    post.save()

    # Finally update topic
    topic.last_message = post
    topic.save()


def create_tutorial_topic(tutorial):
    """Create a new topic for a tutorial.

    Args:
        tutorial: tutorial instance to create a dedicated topic for

    """

    # Text to be displayed to users, with a link to the tutorial
    with open('templates/bot/new_tutorial.html', 'r') as f:
        t = Template(f.read())

    text = t.render(Context({'tutorial': tutorial}))

    # Create topic
    create_topic(
        BOT_TUTORIAL_FORUM_PK, u'[Tutoriel] {}'.format(tutorial.title),
        tutorial.description, text)


def create_article_topic(article):
    """Create a new topic for an article.

    Args:
        article: article instance to create a dedicated topic for

    """

    # Text to be displayed to users, with a link to the article
    with open('templates/bot/new_article.html', 'r') as f:
        t = Template(f.read())

    text = t.render(Context({'article': article}))

    # Create topic
    create_topic(
        BOT_ARTICLE_FORUM_PK, u'[Article] {}'.format(article.title),
        article.description, text)
