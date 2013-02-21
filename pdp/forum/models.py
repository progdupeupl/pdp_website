# coding: utf-8

from math import ceil

from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

from pdp.utils import get_current_user

POSTS_PER_PAGE = 10

class Category(models.Model):
    '''A category, containing forums'''
    class Meta:
        verbose_name = 'Catégorie'
        verbose_name_plural = 'Catégories'

    title = models.CharField('Titre', max_length=80)

    def __unicode__(self):
        '''Textual form of a category'''
        return self.title

    def get_absolute_url(self):
        return '/forums/%s-%s/' % (self.pk, slugify(self.title))

    def get_forums(self):
        return Forum.objects.all().filter(category=self)


class Forum(models.Model):
    '''A forum, containing threads'''
    class Meta:
        verbose_name = 'Forum'
        verbose_name_plural = 'Forums'

    title = models.CharField('Titre', max_length=80)
    subtitle = models.CharField('Sous-titre', max_length=200)

    category = models.ForeignKey(Category, verbose_name='Catégorie')

    def __unicode__(self):
        '''Textual form of a forum'''
        return self.title

    def get_absolute_url(self):
        return '/forums/%s-%s/%s-%s/' % (
            self.category.pk,
            slugify(self.category.title),
            self.pk,
            slugify(self.title),
        )

    def get_topic_count(self):
        '''Gets the number of threads in the forum'''
        return Topic.objects.all().filter(forum__pk=self.pk).count()

    def get_last_message(self):
        '''Gets the last message on the forum, if there are any'''
        try:
            return Post.objects.all().filter(topic__forum__pk=self.pk).order_by('-pubdate')[0]
        except IndexError:
            return None


class Topic(models.Model):
    '''A thread, containing posts'''
    class Meta:
        verbose_name = 'Sujet'
        verbose_name_plural = 'Sujets'

    title = models.CharField('Titre', max_length=80)
    subtitle = models.CharField('Sous-titre', max_length=200)

    forum = models.ForeignKey(Forum, verbose_name='Forum')
    author = models.ForeignKey(User, verbose_name='Auteur')
    last_message = models.ForeignKey('Post', null=True, related_name='last_message', verbose_name='Dernier message')
    pubdate = models.DateTimeField('Date de création', auto_now_add=True)

    is_solved = models.BooleanField('Est résolu')
    is_locked = models.BooleanField('Est verrouillé')
    is_sticky = models.BooleanField('Est en post-it')

    def __unicode__(self):
        '''Textual form of a thread'''
        return self.title

    def get_absolute_url(self):
        return '/forums/sujet/%s-%s' % (self.pk, slugify(self.title))

    def get_post_count(self):
        '''Gets the number of posts in the thread'''
        return Post.objects.all().filter(topic__pk=self.pk).count()

    def get_last_answer(self):
        '''Gets the last answer in the thread, if there are any'''
        try:
            return Post.objects.all().filter(topic__pk=self.pk).order_by('-pubdate')[0]
        except IndexError:
            return None

    def first_post(self):
        return Post.objects.filter(topic=self)[0]

    def last_read_post(self):
        try:
            return TopicRead.objects\
                .select_related()\
                .filter(topic=self, user=get_current_user())\
                .latest('post__pubdate').post
        except Post.DoesNotExist:
            return self.first_post()


class Post(models.Model):
    '''A forum post'''
    topic = models.ForeignKey(Topic, verbose_name='Sujet')
    author = models.ForeignKey(User, verbose_name='Auteur')
    text = models.TextField('Texte')

    pubdate = models.DateTimeField('Date de publication', auto_now_add=True)
    update = models.DateTimeField('Date d\'édition', null=True, blank=True)

    position_in_topic = models.IntegerField('Position dans le sujet')

    is_useful = models.BooleanField('Est utile', default=False)

    def __unicode__(self):
        '''Textual form of a post'''
        return u'<Post pour %s, %s>' % (self.topic, self.pk)

    def get_absolute_url(self):
        page = int(ceil(float(self.position_in_topic) / POSTS_PER_PAGE))

        return '%s?page=%s#p%s' % (self.topic.get_absolute_url(), page, self.pk)


class TopicRead(models.Model):
    topic = models.ForeignKey(Topic)
    post = models.ForeignKey(Post)
    user = models.ForeignKey(User)


def never_read(topic):
    return TopicRead.objects\
        .filter(post=topic.last_message, topic=topic, user=get_current_user())\
        .count() == 0


def mark_read(topic):
    TopicRead.objects.filter(topic=topic, user=get_current_user()).delete()
    t = TopicRead(
        post=topic.last_message, topic=topic, user=get_current_user())
    t.save()
