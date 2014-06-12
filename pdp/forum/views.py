# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

import json
from datetime import datetime

from django.conf import settings
from django.shortcuts import redirect, get_object_or_404
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.decorators.http import require_POST

from pdp.utils import render_template, slugify
from pdp.utils.paginator import paginator_range

from pdp.forum.models import Category, Forum, Topic, Post
from pdp.forum.models import never_read, mark_read
from pdp.forum.models import follow
from pdp.forum.forms import TopicForm, PostForm


def index(request):
    """Display the category list with all their forums.

    Returns:
        HttpResponse

    """
    categories = Category.objects.all().order_by('position')

    return render_template('forum/index.html', {
        'categories': categories
    })


def details(request, cat_slug, forum_slug):
    """Display the given forum and all its topics.

    Returns:
        HttpResponse

    """
    forum = get_object_or_404(Forum, slug=forum_slug)

    sticky_topics = Topic.objects.all()\
        .filter(forum__pk=forum.pk, is_sticky=True)\
        .order_by('-last_message__pubdate')
    topics = Topic.objects.all()\
        .filter(forum__pk=forum.pk, is_sticky=False)\
        .order_by('-last_message__pubdate')

    # Paginator
    paginator = Paginator(topics, settings.TOPICS_PER_PAGE)
    page = request.GET.get('page')

    try:
        shown_topics = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        shown_topics = paginator.page(1)
        page = 1
    except EmptyPage:
        shown_topics = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render_template('forum/details.html', {
        'forum': forum, 'sticky_topics': sticky_topics, 'topics': shown_topics,
        'pages': paginator_range(page, paginator.num_pages), 'nb': page
    })


def cat_details(request, cat_slug):
    """Display the forums belonging to the given category.

    Returns:
        HttpResponse

    """
    category = get_object_or_404(Category, slug=cat_slug)
    forums = Forum.objects.all().filter(category__pk=category.pk)

    return render_template('forum/cat_details.html', {
        'category': category, 'forums': forums
    })


def topic(request, topic_pk, topic_slug):
    """Display a thread and its posts using a pager.

    Returns:
        HttpResponse

    """

    # TODO: Clean that up
    g_topic = get_object_or_404(Topic, pk=topic_pk)

    # Check link
    if not topic_slug == slugify(g_topic.title):
        return redirect(g_topic.get_absolute_url())

    # We mark the topic as read
    if request.user.is_authenticated():
        if never_read(g_topic):
            mark_read(g_topic)

    posts = Post.objects.all()\
        .filter(topic__pk=g_topic.pk)\
        .order_by('position_in_topic')

    last_post_pk = g_topic.last_message.pk

    # Handle pagination
    paginator = Paginator(posts, settings.POSTS_PER_PAGE)

    # The category list is needed to move threads
    categories = Category.objects.all()

    # We try to get page number
    try:
        page_nbr = int(request.GET['page'])
    except KeyError:
        page_nbr = 1

    # We try to page content
    try:
        posts = paginator.page(page_nbr)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        raise Http404

    res = []
    if page_nbr > 1:
        # Show the last post of the previous page
        last_page = paginator.page(page_nbr - 1).object_list
        last_post = (last_page)[len(last_page) - 1]
        res.append(last_post)

    for post in posts:
        res.append(post)

    return render_template('forum/topic.html', {
        'topic': g_topic, 'posts': res, 'categories': categories,
        'pages': paginator_range(page_nbr, paginator.num_pages),
        'nb': page_nbr,
        'last_post_pk': last_post_pk
    })


@login_required(redirect_field_name='suivant')
def new(request):
    """Creates a new topic in a forum.

    Returns:
        HttpResponse

    """
    try:
        forum_pk = request.GET['forum']
    except KeyError:
        raise Http404

    forum = get_object_or_404(Forum, pk=forum_pk)

    if request.method == 'POST':
        form = TopicForm(request.POST)

        if 'preview' in request.POST:
            return render_template('forum/new.html', {
                'forum': forum,
                'form': form,
                'text': form.data['text']
            })

        if form.is_valid():
            data = form.data
            # Creating the thread
            n_topic = Topic()
            n_topic.forum = forum
            n_topic.title = data['title']
            n_topic.subtitle = data['subtitle']
            n_topic.pubdate = datetime.now()
            n_topic.author = request.user
            n_topic.save()

            # Adding the first message
            post = Post()
            post.topic = n_topic
            post.author = request.user
            post.text = data['text']
            post.pubdate = datetime.now()
            post.position_in_topic = 1
            post.save()

            # Updating the topic
            n_topic.last_message = post
            n_topic.save()

            # Make the current user to follow his created topic
            follow(n_topic)

            return redirect(n_topic.get_absolute_url())
    else:
        form = TopicForm()

    return render_template('forum/new.html', {
        'form': form, 'forum': forum
    })


@require_POST
@login_required(redirect_field_name='suivant')
def edit(request):
    """Edit a topic.

    Returns:
        HttpResponse

    """
    try:
        topic_pk = request.POST['topic']
    except KeyError:
        raise Http404

    try:
        page = int(request.POST['page'])
    except KeyError:
        page = 1

    data = request.POST
    resp = {}

    g_topic = get_object_or_404(Topic, pk=topic_pk)

    if request.user.is_authenticated():
        # User actions
        if 'follow' in data:
            resp['follow'] = follow(g_topic)

    if request.user == g_topic.author:
        # Author actions
        if 'solved' in data:
            g_topic.is_solved = not g_topic.is_solved
            resp['solved'] = g_topic.is_solved

    if request.user.has_perm('forum.change_topic'):
        # Staff actions using AJAX, we are using the op_ prefix in order to
        # distinguish staff commands from user commands, since staff commands
        # need to be parsed differently since we are using some tricky JS to
        # retrieve the value of the Foundation switch buttons.
        if 'op_lock' in data:
            g_topic.is_locked = data['op_lock'] == 'true'
        if 'op_sticky' in data:
            g_topic.is_sticky = data['op_sticky'] == 'true'
        if 'op_solved' in data:
            g_topic.is_solved = data['op_solved'] == 'true'
        if 'move' in data:
            try:
                forum_pk = int(request.POST['move_target'])
            except KeyError:
                raise Http404

            forum = get_object_or_404(Forum, pk=forum_pk)
            g_topic.forum = forum

    # Save the changes made on the topic
    g_topic.save()

    if request.is_ajax():
        # If our request is made with AJAX, we return a JSON document in order
        # to update the buttons on the same page without reolading it.
        resp = {
            'lock': g_topic.is_locked,
            'sticky': g_topic.is_sticky,
            'solved': g_topic.is_solved,
            'follow': g_topic.is_followed(request.user),
        }
        return HttpResponse(json.dumps(resp), content_type='application/json')

    else:
        # Elsewise this is a regular POST request so we redirect the user back
        # to the topic.
        return redirect(u'{}?page={}'.format(g_topic.get_absolute_url(), page))


@login_required(redirect_field_name='suivant')
def answer(request):
    """Adds an answer from an user to a topic.

    Returns:
        HttpResponse

    """
    try:
        topic_pk = request.GET['sujet']
    except KeyError:
        raise Http404

    g_topic = get_object_or_404(Topic, pk=topic_pk)
    posts = Post.objects.filter(topic=g_topic).order_by('-pubdate')[:3]
    last_post_pk = g_topic.last_message.pk

    # Making sure posting is allowed
    if g_topic.is_locked:
        raise Http404

    # Check that the user isn't spamming
    if g_topic.antispam(request.user):
        raise Http404

    # If we just sent data
    if request.method == 'POST':
        data = request.POST
        newpost = last_post_pk != int(data['last_post'])

        # Using the « preview button », the « more » button or new post
        if 'preview' in data or 'more' in data or newpost:
            return render_template('forum/answer.html', {
                'text': data['text'], 'topic': g_topic, 'posts': posts,
                'last_post_pk': last_post_pk, 'newpost': newpost
            })

        # Saving the message
        else:
            form = PostForm(request.POST)
            if form.is_valid():
                data = form.data

                post = Post()
                post.topic = g_topic
                post.author = request.user
                post.text = data['text']
                post.pubdate = datetime.now()
                post.position_in_topic = g_topic.get_post_count() + 1
                post.save()

                g_topic.last_message = post
                g_topic.save()

                # Follow topic on answering
                if not g_topic.is_followed():
                    follow(g_topic)

                return redirect(post.get_absolute_url())
            else:
                raise Http404

    else:
        text = ''

        # Using the quote button
        if 'cite' in request.GET:
            post_cite_pk = request.GET['cite']
            post_cite = Post.objects.get(pk=post_cite_pk)

            for line in post_cite.text.splitlines():
                text = text + '> ' + line + '\n'

            text = u'**{0} a écrit :**\n{1}\n'.format(
                post_cite.author.username, text)

        return render_template('forum/answer.html', {
            'topic': g_topic, 'text': text, 'posts': posts,
            'last_post_pk': last_post_pk
        })


@login_required(redirect_field_name='suivant')
def edit_post(request):
    """Edit a specific post.

    Returns:
        HttpResponse

    """
    try:
        post_pk = request.GET['message']
    except KeyError:
        raise Http404

    post = get_object_or_404(Post, pk=post_pk)

    # If we are editing the first post, we also want to edit the topic
    g_topic = None
    if post.position_in_topic == 1:
        g_topic = get_object_or_404(Topic, pk=post.topic.pk)

    # Making sure the user is allowed to do that
    if post.author != request.user:
        if not request.user.has_perm('forum.change_post'):
            raise Http404
        elif request.method == 'GET':
            messages.add_message(
                request, messages.WARNING,
                u'Vous éditez ce message en tant que modérateur (auteur : {}).'
                u' Soyez encore plus prudent lors de l\'édition de celui-ci !'
                .format(post.author.username))

    if request.method == 'POST':

        # Using the preview button
        if 'preview' in request.POST:
            if g_topic:
                g_topic = Topic(title=request.POST['title'],
                                subtitle=request.POST['subtitle'])
            return render_template('forum/edit_post.html', {
                'post': post, 'topic': g_topic, 'text': request.POST['text'],
            })

        # The user just sent data, handle them
        post.text = request.POST['text']
        post.update = datetime.now()
        post.save()

        # Modifying the thread info
        if g_topic:
            g_topic.title = request.POST['title']
            g_topic.subtitle = request.POST['subtitle']
            g_topic.save()

        return redirect(post.get_absolute_url())

    else:
        return render_template('forum/edit_post.html', {
            'post': post, 'topic': g_topic, 'text': post.text
        })


@login_required(redirect_field_name='suivant')
def useful_post(request):
    """Marks a message as useful for the original poster.

    Returns:
        HttpResponse

    """
    try:
        post_pk = request.GET['message']
    except KeyError:
        raise Http404

    post = get_object_or_404(Post, pk=post_pk)

    # Making sure the user is allowed to do that
    if post.author == request.user or request.user != post.topic.author:
        raise Http404

    post.is_useful = not post.is_useful
    post.save()

    return redirect(post.get_absolute_url())


def find_topic(request, name):
    """Find all topics created by an user.

    Returns:
        HttpResponse

    """
    u = get_object_or_404(User, username=name)

    topics = Topic.objects.all().filter(author=u)\
                          .order_by('-pubdate')

    # Paginator
    paginator = Paginator(topics, settings.TOPICS_PER_PAGE)
    page = request.GET.get('page')

    try:
        shown_topics = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        shown_topics = paginator.page(1)
        page = 1
    except EmptyPage:
        shown_topics = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render_template('forum/find_topic.html', {
        'topics': shown_topics, 'usr': u,
        'pages': paginator_range(page, paginator.num_pages), 'nb': page
    })


def find_post(request, name):
    """Find all posts written by an user.

    Returns:
        HttpResponse

    """
    u = get_object_or_404(User, username=name)

    posts = Post.objects.all().filter(author=u)\
        .order_by('-pubdate')

    paginator = Paginator(posts, settings.POSTS_PER_PAGE)
    page = request.GET.get('page')

    try:
        shown_posts = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        shown_posts = paginator.page(1)
        page = 1
    except EmptyPage:
        shown_posts = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render_template('forum/find_post.html', {
        'posts': shown_posts, 'usr': u,
        'pages': paginator_range(page, paginator.num_pages), 'nb': page
    })


@login_required(redirect_field_name='suivant')
def followed_topics(request):
    """Displays all the topics followed by an user.

    Returns:
        HttpResponse

    """
    followed_topics = request.user.get_profile().get_followed_topics()

    # Paginator
    paginator = Paginator(followed_topics, settings.FOLLOWED_TOPICS_PER_PAGE)
    page = request.GET.get('page')

    try:
        shown_topics = paginator.page(page)
        page = int(page)
    except PageNotAnInteger:
        shown_topics = paginator.page(1)
        page = 1
    except EmptyPage:
        shown_topics = paginator.page(paginator.num_pages)
        page = paginator.num_pages

    return render_template('forum/followed_topics.html', {
        'followed_topics': shown_topics,
        'pages': paginator_range(page, paginator.num_pages),
        'nb': page
    })


# Deprecated URLs

def deprecated_topic_redirect(request, topic_pk, topic_slug):
    topic = get_object_or_404(Topic, pk=topic_pk)
    return redirect(topic.get_absolute_url(), permanent=True)


def deprecated_cat_details_redirect(request, cat_pk, cat_slug):
    category = get_object_or_404(Category, pk=cat_pk)
    return redirect(category.get_absolute_url(), permanent=True)


def deprecated_details_redirect(request, cat_slug, forum_pk, forum_slug):
    forum = get_object_or_404(Forum, pk=forum_pk)
    return redirect(forum.get_absolute_url(), permanent=True)


def deprecated_feed_messages_rss(request):
    return redirect('/forums/flux/messages/rss/', permanent=True)


def deprecated_feed_messages_atom(request):
    return redirect('/forums/flux/messages/atom/', permanent=True)
