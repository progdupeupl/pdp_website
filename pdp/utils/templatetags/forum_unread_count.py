# coding: utf-8

from django import template

from pdp.forum.models import Topic, never_read

register = template.Library()


@register.filter('forum_unread_count')
def forum_unread_count(user):
    count = 0

    topics = Topic.objects.all()
    for topic in topics:
        if never_read(topic, user):
            count = count + 1

    return count
