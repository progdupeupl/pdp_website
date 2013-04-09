# coding: utf-8

from django import template

from pdp.forum.models import TopicFollowed, never_read

register = template.Library()


@register.filter('interventions_topics_count')
def interventions_topics_count(user):
    topicsfollowed = TopicFollowed.objects.filter(user=user)
    count = 0
    for topicfollowed in topicsfollowed:
        if never_read(topicfollowed.topic):
            count += 1
    return count


@register.filter('interventions_topics')
def interventions_topics(user):
    topicsfollowed = TopicFollowed.objects.filter(user=user)\
        .order_by('-topic__last_message__pubdate')
    topics_unread = []
    topics_read = []

    for topicfollowed in topicsfollowed:
        if never_read(topicfollowed.topic):
            topics_unread.append(topicfollowed.topic)
        else:
            topics_read.append(topicfollowed.topic)

    return {'unread': topics_unread,
            'read': topics_read[:5 - len(topics_unread)]}
