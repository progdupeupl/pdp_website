# coding: utf-8

from datetime import datetime

from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

from django.contrib.auth.decorators import login_required

from pdp.utils import render_template, slugify

from .models import Article, get_prev_article, get_next_article
from .forms import ArticleForm

def index(request):
    '''Displayy articles list'''
    article = Article.objects.all()\
        .filter(is_visible=True)\
        .order_by('-pubdate')

    if request.user.is_authenticated():
        user_article = Article.objects.filter(author=request.user)
    else:
        user_article = None

    return render_template('article/index.html', {
        'articles': article,
        'user_articles': user_article
    })


def view(request, article_pk, article_slug):
    '''Show the given article if exists and is visible'''
    article = get_object_or_404(Article, pk=article_pk)

    if not article.is_visible and not request.user == article.author:
        raise Http404

    if article_slug != slugify(article.title):
        return redirect(article.get_absolute_url())

    return render_template('article/view.html', {
        'article': article,
        'prev': get_prev_article(article),
        'next': get_next_article(article)
    })


@login_required
def new(request):
    '''Create a new article'''
    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.data

            article = Article()
            article.title = data['title']
            article.description = data['description']
            article.text = data['text']
            article.author = request.user
            if 'image' in request.FILES :
                article.image = request.FILES['image']

            # Since the article is not published yet, this value isn't
            # important (will be changed on publish)
            article.pubdate = datetime.now()

            # First save before tags because they need to know the id of the
            # article
            article.save()

            list_tags = data['tags'].split(',')
            for tag in list_tags:
                article.tags.add(tag)
            article.save()
            return redirect(article.get_absolute_url())
    else:
        form = ArticleForm()

    return render_template('article/new.html', {
        'form': form
    })


@login_required
def edit(request):
    '''Edit article identified by given GET paramter'''
    try:
        article_pk = request.GET['article']
    except KeyError:
        raise Http404

    article = get_object_or_404(Article, pk=article_pk)

    # Make sure the user is allowed to do it
    if not request.user == article.author:
        raise Http404

    if request.method == 'POST':
        form = ArticleForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.data

            article.title = data['title']
            article.description = data['description']
            article.text = data['text']
            if 'image' in request.FILES:
                article.image = request.FILES['image']

            article.tags.clear()
            list_tags = data['tags'].split(',')
            for tag in list_tags:
                article.tags.add(tag)

            article.save()
            return redirect(article.get_absolute_url())
    else:
        # initial value for tags input
        list_tags = ''
        for tag in article.tags.all():
            list_tags += ',' + tag.__str__()

        form = ArticleForm({
            'title': article.title,
            'description': article.description,
            'text': article.text,
            'tags': list_tags,
        })

    return render_template('article/edit.html', {
        'article': article, 'form': form
    })


@login_required
def modify(request):
    if not request.method == 'POST':
        raise Http404

    data = request.POST

    article_pk = data['article']
    article = get_object_or_404(Article, pk=article_pk)

    if request.user == article.author:
        if 'delete' in data:
            article.delete()
            return redirect('/articles/')

    return redirect(article.get_absolute_url())


# Deprecated URLs

def deprecated_view_redirect(request, article_pk, article_slug):
    article = get_object_or_404(Article, pk=article_pk)
    return redirect(article.get_absolute_url(), permanent=True)
