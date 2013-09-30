# coding: utf-8

from django import template

from pdp.forum.models import TopicFollowed, never_read

register = template.Library()


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

    read_topics_count = 5 - (len(topics_unread) if len(topics_unread) < 5 else 5)
    return {'unread': topics_unread,
            'read': topics_read[:read_topics_count]}

@register.simple_tag(name='reads_topic')
def reads_topic(topic, user):
    if user.is_authenticated() :
        if never_read (topic, user) :
            return ''
        else :
            return 'secondary'
    else :
        return '';
    