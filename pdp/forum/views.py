# coding: utf-8

from datetime import datetime

from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from pdp.utils import render_template, slugify

from models import Category, Forum, Topic, Post, POSTS_PER_PAGE
from models import never_read, mark_read
from forms import TopicForm, PostForm


def index(request):
    '''Affiche la liste des forums'''
    c = Category.objects.all()

    return render_template('forum/index.html', {
        'categories': c
    })


def details(request, cat_slug, forum_pk, forum_slug):
    '''Affiche la liste des sujets d'un forum'''
    f = get_object_or_404(Forum, pk=forum_pk)

    t = Topic.objects.all()\
        .filter(forum__pk=f.pk)\
        .order_by('-is_sticky', '-last_message__pubdate')

    # Check link
    if not cat_slug == slugify('%s-%s' % (f.category.pk, f.category.title))\
            or not forum_slug == slugify(f.title):
        return redirect(f.get_absolute_url())

    return render_template('forum/details.html', {
        'forum': f, 'topics': t
    })


def cat_details(request, cat_pk, cat_slug):
    '''Affiche la liste des forums reliés à une catégorie précise'''
    c = get_object_or_404(Category, pk=cat_pk)
    f = Forum.objects.all().filter(category__pk=c.pk)

    # Check link
    if not cat_slug == slugify(c.title):
        return redirect(c.get_absolute_url())

    return render_template('forum/cat_details.html', {
        'category': c, 'forums': f
    })


def topic(request, topic_pk, topic_slug):
    '''Visualisation d'un sujet et de ses réponses'''

    # TODO: Clean that up
    t = get_object_or_404(Topic, pk=topic_pk)

    if request.user.is_authenticated():
        if never_read(t):
            mark_read(t)

    posts = Post.objects.all().filter(topic__pk=t.pk).order_by('position_in_topic')

    # Handle pagination
    paginator = Paginator(posts, POSTS_PER_PAGE)

    # The category list is needed to move threads
    categories = Category.objects.all()

    try:
        nb = int(request.GET['page'])
    except KeyError:
        nb = 1

    try:
        p = paginator.page(nb)
    except PageNotAnInteger:
        p = paginator.page(1)
    except EmptyPage:
        raise Http404

    # Check link
    if not topic_slug == slugify(t.title):
        return redirect(t.get_absolute_url())

    res = []
    if nb != 1:
        # Show the last post of the previous page
        last_page = paginator.page(nb - 1).object_list
        last_post = (last_page)[len(last_page) - 1]
        res.append(last_post)

    [res.append(post) for post in p]

    return render_template('forum/topic.html', {
        'topic': t, 'posts': res, 'categories': categories,
        'pages': [i for i in range(1, paginator.num_pages + 1)], 'nb': nb,
    })


@login_required
def new(request):

    try:
        forum_pk = request.GET['forum']
    except KeyError:
        raise Http404

    forum = get_object_or_404(Forum, pk=forum_pk)

    if request.method == 'POST':

        # If the client is using the "preview" button
        if 'preview' in request.POST:
            return render_template('forum/new.html', {
                'forum': forum,
                'title': request.POST['title'],
                'subtitle': request.POST['subtitle'],
                'text': request.POST['text'],
            })

        form = TopicForm(request.POST)
        if form.is_valid():
            try:
                f = Forum.objects.get(pk=forum_pk)
            except Forum.DoesNotExists:
                raise Http404
            data = form.data

            # Creating the thread
            t = Topic()
            t.forum = f
            t.title = data['title']
            t.subtitle = data['subtitle']
            t.pubdate = datetime.now()
            t.author = request.user
            t.save()

            # Adding the first message
            p = Post()
            p.topic = t
            p.author = request.user
            p.text = data['text']
            p.pubdate = datetime.now()
            p.position_in_topic = 1
            p.save()

            t.last_message = p
            t.save()

            return redirect(t.get_absolute_url())

        else:
            # TODO: add errors to the form and return it
            raise Http404

    else:

        form = TopicForm()
        return render_template('forum/new.html', {
            'form': form, 'forum': forum
        })


@login_required
def edit(request):
    if not request.method == 'POST':
        raise Http404

    try:
        topic_pk = request.POST['topic']
    except KeyError:
        raise Http404

    data = request.POST

    t = get_object_or_404(Topic, pk=topic_pk)

    if not request.user == t.author and not request.user.is_staff:
        return Http404

    if 'solved' in data:
        t.is_solved = not t.is_solved
    elif request.user.is_staff:
        if 'lock' in data:
            t.is_locked = not t.is_locked
        elif 'sticky' in data:
            t.is_sticky = not t.is_sticky
        elif 'follow' in data:
            raise NotImplementedError
        elif 'move' in data:
            try:
                forum_pk = int(request.POST['move_target'])
            except KeyError:
                raise Http404

            forum = get_object_or_404(Forum, pk=forum_pk)
            t.forum = forum
        else:
            # The admin task doesn't exist
            raise Http404
    else:
        # The user task doesn't exist
        raise Http404

    t.save()
    return redirect(t.get_absolute_url())


@login_required
def answer(request):
    'Ajoute une réponse à une discussion'
    try:
        topic_pk = request.GET['sujet']
    except KeyError:
        raise Http404

    t = get_object_or_404(Topic, pk=topic_pk)

    # Making sure posting is allowed
    if t.is_locked:
        raise Http404

    # If we just sent data
    if request.method == 'POST':

        # Using the "preview" button or the "more options" button
        if 'preview' in request.POST or 'plus' in request.GET:
            text = request.POST['text']
            return render_template('forum/answer.html', {
                'text': text, 'topic': t
            })

        # Saving the message
        else:
            form = PostForm(request.POST)
            if form.is_valid():
                data = form.data

                p = Post()
                p.topic = t
                p.author = request.user
                p.text = data['text']
                p.pubdate = datetime.now()
                p.position_in_topic = t.get_post_count() + 1
                p.save()

                t.last_message = p
                t.save()

                return redirect(p.get_absolute_url())
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

            text = u'**%s a écrit :**\n%s\n' % (
                post_cite.author.username, text)

        return render_template('forum/answer.html', {
            'topic': t, 'text': text
        })


@login_required
def edit_post(request):
    try:
        post_pk = request.GET['message']
    except KeyError:
        raise Http404

    post = get_object_or_404(Post, pk=post_pk)

    topic = None
    if post.position_in_topic == 1:
        topic = get_object_or_404(Topic, pk=post.topic.pk)

    # Making sure the user is allowed to do that
    if post.author != request.user and not request.user.is_staff:
        raise Http404

    if request.method == 'POST':

        # Using the preview button
        if 'preview' in request.POST:
            if topic:
                topic = Topic(title=request.POST['title'], subtitle=request.POST['subtitle'])
            return render_template('forum/edit_post.html', {
                'post': post, 'topic': topic, 'text': request.POST['text'],
            })

        # The user just sent data, handle them
        post.text = request.POST['text']
        post.update = datetime.now()
        post.save()

        # Modifying the thread info
        if topic:
            topic.title = request.POST['title']
            topic.subtitle = request.POST['subtitle']
            topic.save()

        return redirect(post.get_absolute_url())

    else:
        return render_template('forum/edit_post.html', {
            'post': post, 'topic': topic, 'text': post.text
        })


@login_required
def useful_post(request):
    '''Marque un message comme ayant été utile pour l'OP'''
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
