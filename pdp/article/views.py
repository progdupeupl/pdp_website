# coding: utf-8

from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

from django.contrib.auth.decorators import login_required

from pdp.utils import render_template, slugify

from .models import Article
from .forms import ArticleForm


def index(request):
    a = Article.objects.all().filter(is_visible=True)

    if request.user.is_authenticated():
        user_a = Article.objects.filter(author=request.user)
    else:
        user_a = None

    return render_template('article/index.html', {
        'articles': a,
        'user_articles': user_a
    })


def view(request, article_pk, article_slug):

    a = get_object_or_404(Article, pk=article_pk)

    if not a.is_visible and not request.user == a.author:
        raise Http404

    if article_slug != slugify(a.title):
        return redirect(a.get_absolute_url())

    return render_template('article/view.html', {
        'article': a
    })


@login_required
def new(request):

    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            data = form.data

            a = Article()
            a.title = data['title']
            a.description = data['description']
            a.text = data['text']
            a.author = request.user
            a.save()

            return redirect(a.get_absolute_url())
    else:
        form = ArticleForm()

    return render_template('article/new.html', {
        'form': form
    })


@login_required
def edit(request):
    try:
        article_pk = request.GET['article']
    except KeyError:
        raise Http404

    a = get_object_or_404(Article, pk=article_pk)

    # On vérifie que l'utilisateur a le droit de faire ça
    if not request.user == a.author:
        raise Http404

    if request.method == 'POST':
        form = ArticleForm(request.POST)

        if form.is_valid():
            data = form.data

            a.title = data['title']
            a.description = data['description']
            a.text = data['text']
            a.save()

            return redirect(a.get_absolute_url())

    else:
        form = ArticleForm({
            'title': a.title,
            'description': a.description,
            'text': a.text
        })

    return render_template('article/edit.html', {
        'article': a, 'form': form
    })
