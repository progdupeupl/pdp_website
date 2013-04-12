# coding: utf-8

from datetime import datetime

from django.shortcuts import redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from pdp.utils import render_template, slugify

from models import Category, Forum, Topic, Post, POSTS_PER_PAGE
from models import never_read, mark_read, clear_forum, clear_forums
from models import follow
from forms import TopicForm, PostForm


def index(request):
    '''
    Display the category list with all their forums
    '''
    categories = Category.objects.all()

    return render_template('forum/index.html', {
        'categories': categories
    })


def details(request, cat_slug, forum_pk, forum_slug):
    '''
    Display the given forum and all its topics
    '''
    forum = get_object_or_404(Forum, pk=forum_pk)

    topics = Topic.objects.all()\
        .filter(forum__pk=forum.pk)\
        .order_by('-is_sticky', '-last_message__pubdate')

    # Check that given URL is correct, otherwise redirect to the good one
    if not cat_slug == slugify('%s-%s' % (forum.category.pk,
                                          forum.category.title))\
            or not forum_slug == slugify(forum.title):
        return redirect(forum.get_absolute_url())

    return render_template('forum/details.html', {
        'forum': forum, 'topics': topics
    })


def cat_details(request, cat_pk, cat_slug):
    '''
    Display the forums belonging to the given category
    '''
    category = get_object_or_404(Category, pk=cat_pk)
    forums = Forum.objects.all().filter(category__pk=category.pk)

    # Check link
    if not cat_slug == slugify(category.title):
        return redirect(category.get_absolute_url())

    return render_template('forum/cat_details.html', {
        'category': category, 'forums': forums
    })


def topic(request, topic_pk, topic_slug):
    '''
    Display a thread and its posts using a pager
    '''

    # TODO: Clean that up
    g_topic = get_object_or_404(Topic, pk=topic_pk)

    # Check link
    if not topic_slug == slugify(g_topic.title):
        return redirect(g_topic.get_absolute_url())

    if request.user.is_authenticated():
        if never_read(g_topic):
            mark_read(g_topic)

    posts = Post.objects.all().filter(topic__pk=g_topic.pk)\
                              .order_by('position_in_topic')

    last_post_pk = g_topic.last_message.pk

    # Handle pagination
    paginator = Paginator(posts, POSTS_PER_PAGE)

    # The category list is needed to move threads
    categories = Category.objects.all()

    try:
        page_nbr = int(request.GET['page'])
    except KeyError:
        page_nbr = 1

    try:
        posts = paginator.page(page_nbr)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        raise Http404

    res = []
    if page_nbr != 1:
        # Show the last post of the previous page
        last_page = paginator.page(page_nbr - 1).object_list
        last_post = (last_page)[len(last_page) - 1]
        res.append(last_post)

    for post in posts:
        res.append(post)

    return render_template('forum/topic.html', {
        'topic': g_topic, 'posts': res, 'categories': categories,
        'pages': range(1, paginator.num_pages + 1), 'nb': page_nbr,
        'last_post_pk': last_post_pk
    })


@login_required
def new(request):
    '''
    Creates a new topic in a forum
    '''
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

            n_topic.last_message = post
            n_topic.save()

            # Follow the topic
            follow(n_topic)

            return redirect(n_topic.get_absolute_url())

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
    '''
    Edit the given topic
    '''
    if not request.method == 'POST':
        raise Http404

    try:
        topic_pk = request.POST['topic']
    except KeyError:
        raise Http404

    data = request.POST

    g_topic = get_object_or_404(Topic, pk=topic_pk)

    if request.user.is_authenticated():
        # User actions
        if 'follow' in data:
            follow(g_topic)
    if request.user == g_topic.author:
        # Author actions
        if 'solved' in data:
            g_topic.is_solved = not g_topic.is_solved
    if request.user.is_staff:
        # Staff actions
        if 'lock' in data:
            g_topic.is_locked = not g_topic.is_locked
        elif 'sticky' in data:
            g_topic.is_sticky = not g_topic.is_sticky
        elif 'move' in data:
            try:
                forum_pk = int(request.POST['move_target'])
            except KeyError:
                raise Http404

            forum = get_object_or_404(Forum, pk=forum_pk)
            g_topic.forum = forum

    g_topic.save()
    return redirect(g_topic.get_absolute_url())


@login_required
def answer(request):
    '''
    Adds an answer from an user to a topic
    '''
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
        if 'preview' in data or 'plus' in request.GET or newpost:
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

            text = u'**%s a écrit :**\n%s\n' % (
                post_cite.author.username, text)

        return render_template('forum/answer.html', {
            'topic': g_topic, 'text': text, 'posts': posts,
            'last_post_pk': last_post_pk
        })


@login_required
def edit_post(request):
    '''
    Edit the given user's post
    '''
    try:
        post_pk = request.GET['message']
    except KeyError:
        raise Http404

    post = get_object_or_404(Post, pk=post_pk)

    g_topic = None
    if post.position_in_topic == 1:
        g_topic = get_object_or_404(Topic, pk=post.topic.pk)

    # Making sure the user is allowed to do that
    if post.author != request.user and not request.user.is_staff:
        raise Http404

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


@login_required
def useful_post(request):
    '''Marks a message as useful (for the OP)'''
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


@login_required
def clear(request):
    '''
    Clear forums by marking all topics of one or all forums as read by the user
    '''

    if not request.method == 'POST':
        raise Http404

    try:
        target = request.POST['clear_target']
    except KeyError:
        raise Http404

    if target == 'all':
        # Clear all forums
        clear_forums()
        return redirect('/forums/')
    else:
        # Clear only the forum passed via POST field
        forum_pk = int(target)
        forum = get_object_or_404(Forum, pk=forum_pk)
        clear_forum(forum)
        return rediathreadrect(forum.get_absolute_url())
