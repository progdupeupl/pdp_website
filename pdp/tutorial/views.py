# coding: utf-8

from datetime import datetime

from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pdp.utils import render_template, slugify
from pdp.utils.tutorials import move, export_tutorial

from .models import Tutorial, Part, Chapter, Extract
from .forms import TutorialForm, EditTutorialForm, PartForm, ChapterForm, \
    EmbdedChapterForm, ExtractForm, EditExtractForm


def index(request):
    '''Display tutorials list'''
    tutorials = Tutorial.objects.all()\
            .filter(is_visible=True)\
            .order_by("-pubdate")

    if request.user.is_authenticated():
        user_tutorials = Tutorial.objects.filter(authors=request.user)
    else:
        user_tutorials = None

    return render_template('tutorial/index.html', {
        'tutorials': tutorials,
        'user_tutorials': user_tutorials
    })


# Tutorial

def view_tutorial(request, tutorial_pk, tutorial_slug):
    '''Display a tutorial'''
    tutorial = get_object_or_404(Tutorial, pk=tutorial_pk)

    if not tutorial.is_visible and request.user not in tutorial.authors.all():
        raise Http404

    # Make sure the URL is well-formed
    if not tutorial_slug == slugify(tutorial.title):
        return redirect(tutorial.get_absolute_url())

    # Two variables to handle two distinct cases (large/small tutorial)
    chapter = None
    parts = None

    # If it's a small tutorial, fetch its chapter
    if tutorial.is_mini:
        chapter = Chapter.objects.get(tutorial=tutorial)
    else:
        parts = Part.objects.all(
        ).filter(tutorial=tutorial).order_by('position_in_tutorial')

    return render_template('tutorial/view_tutorial.html', {
        'tutorial': tutorial, 'chapter': chapter, 'parts': parts
    })


def download(request):
    '''Download a tutorial'''
    import json

    tutorial = get_object_or_404(Tutorial, pk=request.GET['tutoriel'])

    if not tutorial.is_visible and not request.user in tutorial.authors.all():
        raise Http404

    dct = export_tutorial(tutorial)
    data = json.dumps(dct, indent=4, ensure_ascii=False)

    response = HttpResponse(data, mimetype='application/json')
    response['Content-Disposition'] = 'attachment; filename={0}.json'.format(tutorial.slug)

    return response


@login_required
def add_tutorial(request):
    ''''Adds a tutorial'''
    if request.method == 'POST':
        form = TutorialForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.data
            # Creating a tutorial
            tutorial = Tutorial()
            tutorial.title = data['title']
            tutorial.description = data['description']
            tutorial.is_mini = 'is_mini' in data
            tutorial.pubdate = datetime.now()
            tutorial.save()

            # We need to save the tutorial before changing its author list
            # since it's a many-to-many relationship
            tutorial.authors.add(request.user)
            # Save the icon
            if 'icon' in request.FILES:
                tutorial.icon = request.FILES['icon']
            tutorial.save()
            # If it's a small tutorial, create its corresponding chapter
            if tutorial.is_mini:
                chapter = Chapter()
                chapter.tutorial = tutorial
                chapter.save()

            return redirect(tutorial.get_absolute_url())
    else:
        form = TutorialForm()

    return render_template('tutorial/new_tutorial.html', {
        'form': form
    })


@login_required
def edit_tutorial(request):
    try:
        tutorial_pk = request.GET['tutoriel']
    except KeyError:
        raise Http404

    tutorial = get_object_or_404(Tutorial, pk=tutorial_pk)

    if not request.user in tutorial.authors.all():
        raise Http404

    if request.method == 'POST':
        form = EditTutorialForm(request.POST)
        if form.is_valid():
            data = form.data
            tutorial.title = data['title']
            tutorial.description = data['description']
            tutorial.introduction = data['introduction']
            tutorial.conclusion = data['conclusion']
            tutorial.save()

            return redirect(tutorial.get_absolute_url())
    else:
        form = EditTutorialForm({
            'title': tutorial.title,
            'description': tutorial.description,
            'introduction': tutorial.introduction,
            'conclusion': tutorial.conclusion
        })

    return render_template('tutorial/edit_tutorial.html', {
        'tutorial': tutorial, 'form': form
    })


def modify_tutorial(request):
    if not request.method == 'POST':
        raise Http404

    tutorial_pk = request.POST['tutorial']
    tutorial = get_object_or_404(Tutorial, pk=tutorial_pk)

    if not request.user in tutorial.authors.all():
        raise Http404

    if 'delete' in request.POST:
        tutorial.delete()
        return redirect('/tutoriels/')

    elif 'add_author' in request.POST:
        redirect_url = reverse(
            'pdp.tutorial.views.edit_tutorial') + '?tutoriel={0}'.format(tutorial.pk)

        author_username = request.POST['author']
        author = None
        try:
            author = User.objects.get(username=author_username)
        except User.DoesNotExist:
            return redirect(redirect_url)

        tutorial.authors.add(author)
        tutorial.save()

        return redirect(redirect_url)

    elif 'remove_author' in request.POST:
        redirect_url = reverse(
            'pdp.tutorial.views.edit_tutorial') + '?tutoriel={0}'.format(tutorial.pk)

        # Avoid orphan tutorials
        if tutorial.authors.all().count() <= 1:
            raise Http404

        author_pk = request.POST['author']
        author = get_object_or_404(User, pk=author_pk)

        tutorial.authors.remove(author)
        tutorial.save()

        return redirect(redirect_url)

    raise Http404


# Part

def view_part(request, tutorial_pk, tutorial_slug, part_slug):
    '''Display a part'''
    part = get_object_or_404(Part,
                             slug=part_slug, tutorial__pk=tutorial_pk)

    tutorial = part.tutorial
    if not tutorial.is_visible and not request.user in \
            tutorial.authors.all():
        raise Http404

    # Make sure the URL is well-formed
    if not tutorial_slug == slugify(tutorial.title)\
            or not part_slug == slugify(part.title):
        return redirect(part.get_absolute_url())

    return render_template('tutorial/view_part.html', {
        'part': part
    })


@login_required
def add_part(request):
    '''Add a new part'''
    try:
        tutorial_pk = request.GET['tutoriel']
    except KeyError:
        raise Http404
    tutorial = get_object_or_404(Tutorial, pk=tutorial_pk)
    # Make sure it's a big tutorial, just in case
    if tutorial.is_mini:
        raise Http404
    # Make sure the user belongs to the author list
    if not request.user in tutorial.authors.all():
        raise Http404
    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            data = form.data
            part = Part()
            part.tutorial = tutorial
            part.title = data['title']
            part.introduction = data['introduction']
            part.conclusion = data['conclusion']
            part.position_in_tutorial = tutorial.get_parts().count() + 1
            part.save()
            return redirect(part.get_absolute_url())
    else:
        form = PartForm()
    return render_template('tutorial/new_part.html', {
        'tutorial': tutorial, 'form': form
    })


@login_required
def modify_part(request):
    '''Modifiy the given part'''
    if not request.method == 'POST':
        raise Http404

    part_pk = request.POST['part']
    part = get_object_or_404(Part, pk=part_pk)

    # Make sure the user is allowed to do that
    if not request.user in part.tutorial.authors.all():
        raise Http404

    if 'move' in request.POST:
        new_pos = int(request.POST['move_target'])
        move(part, new_pos, 'position_in_tutorial', 'tutorial', 'get_parts')
        part.save()

    elif 'delete' in request.POST:
        # Delete all chapters belonging to the part
        Chapter.objects.all().filter(part=part).delete()

        # Move other parts
        old_pos = part.position_in_tutorial
        for tut_p in part.tutorial.get_parts():
            if old_pos <= tut_p.position_in_tutorial:
                tut_p.position_in_tutorial = tut_p.position_in_tutorial - 1
                tut_p.save()

        # Actually delete the part
        part.delete()

    return redirect(part.tutorial.get_absolute_url())


@login_required
def edit_part(request):
    '''Edit the given part'''
    try:
        part_pk = int(request.GET['partie'])
    except KeyError:
        raise Http404
    part = get_object_or_404(Part, pk=part_pk)
    # Make sure the user is allowed to do that
    if not request.user in part.tutorial.authors.all():
        raise Http404

    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            data = form.data
            part.title = data['title']
            part.introduction = data['introduction']
            part.conclusion = data['conclusion']
            part.save()
            return redirect(part.get_absolute_url())
    else:
        form = PartForm({
            'title': part.title,
            'introduction': part.introduction,
            'conclusion': part.conclusion
        })

    return render_template('tutorial/edit_part.html', {
        'part': part, 'form': form
    })


# Chapter

def view_chapter(request, tutorial_pk, tutorial_slug, part_slug,
                 chapter_slug):
    '''View chapter'''

    chapter = get_object_or_404(Chapter,
                                slug=chapter_slug,
                                part__slug=part_slug,
                                part__tutorial__pk=tutorial_pk)

    tutorial = chapter.get_tutorial()
    if not tutorial.is_visible \
            and not request.user in tutorial.authors.all():
        raise Http404

    if not tutorial_slug == slugify(tutorial.title)\
        or not part_slug == slugify(chapter.part.title)\
            or not chapter_slug == slugify(chapter.title):
        return redirect(chapter.get_absolute_url())

    prev_chapter = Chapter.objects.all()\
        .filter(part__tutorial__pk=chapter.part.tutorial.pk)\
        .filter(position_in_tutorial__lt=chapter.position_in_tutorial)\
        .order_by('-position_in_tutorial')
    prev_chapter = prev_chapter[0] if len(prev_chapter) > 0 else None

    next_chapter = Chapter.objects.all()\
        .filter(part__tutorial__pk=chapter.part.tutorial.pk)\
        .filter(position_in_tutorial__gt=chapter.position_in_tutorial)\
        .order_by('position_in_tutorial')
    next_chapter = next_chapter[0] if len(next_chapter) > 0 else None

    return render_template('tutorial/view_chapter.html', {
        'chapter': chapter,
        'prev': prev_chapter,
        'next': next_chapter
    })


@login_required
def add_chapter(request):
    '''Add a new chapter to given part'''
    try:
        part_pk = request.GET['partie']
    except KeyError:
        raise Http404
    part = get_object_or_404(Part, pk=part_pk)

    # Make sure the user is allowed to do that
    if not request.user in part.tutorial.authors.all():
        raise Http404

    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            data = form.data

            # We check that another chapter doesn't exist with the same slug
            already_exist = False
            for p_chapter in part.get_chapters():
                if p_chapter.slug == slugify(data['title']):
                    already_exist = True
                    break

            if not already_exist:
                chapter = Chapter()
                chapter.title = data['title']
                chapter.introduction = data['introduction']
                chapter.conclusion = data['conclusion']
                chapter.part = part
                chapter.position_in_part = part.get_chapters().count() + 1
                chapter.update_position_in_tutorial()
                chapter.save()

                if 'submit_continue' in request.POST:
                    form = ChapterForm()
                    messages.success(request,
                                     u'Chapitre « {0} » ajouté avec succès.'.format( \
                                     chapter.title))
                else:
                    return redirect(chapter.get_absolute_url())
            else:
                messages.error(request, u'Un chapitre portant le même nom '
                                        u'existe déjà dans cette partie.')
    else:
        form = ChapterForm()

    return render_template('tutorial/new_chapter.html', {
        'part': part, 'form': form
    })


@login_required
def modify_chapter(request):
    '''Modify the given chapter'''
    if not request.method == 'POST':
        raise Http404
    data = request.POST
    try:
        chapter_pk = request.POST['chapter']
    except KeyError:
        raise Http404
    chapter = get_object_or_404(Chapter, pk=chapter_pk)

    # Make sure the user is allowed to do that
    if not request.user in chapter.get_tutorial().authors.all():
        raise Http404

    if 'move' in data:
        new_pos = int(request.POST['move_target'])
        move(chapter, new_pos, 'position_in_part', 'part', 'get_chapters')
        chapter.update_position_in_tutorial()
        chapter.save()

    elif 'delete' in data:
        old_pos = chapter.position_in_part
        old_tut_pos = chapter.position_in_tutorial
        # Move other chapters first
        for tut_c in chapter.part.get_chapters():
            if old_pos <= tut_c.position_in_part:
                tut_c.position_in_part = tut_c.position_in_part - 1
                tut_c.save()
        # Then delete the chapter
        chapter.delete()
        # Update all the position_in_tutorial fields for the next chapters
        for tut_c in Chapter.objects\
                .filter(position_in_tutorial__gt=old_tut_pos):
            tut_c.update_position_in_tutorial()
            tut_c.save()

    return redirect(chapter.part.get_absolute_url())


@login_required
def edit_chapter(request):
    '''Edit the given chapter'''

    try:
        chapter_pk = int(request.GET['chapitre'])
    except KeyError:
        raise Http404

    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    big = chapter.part
    small = chapter.tutorial

    # Make sure the user is allowed to do that
    if big and (not request.user in chapter.part.tutorial.authors.all())\
            or small and (not request.user in chapter.tutorial.authors.all()):
        raise Http404

    if request.method == 'POST':

        if chapter.part:
            form = ChapterForm(request.POST)
        else:
            form = EmbdedChapterForm(request.POST)

        if form.is_valid():
            data = form.data
            if chapter.part:
                chapter.title = data['title']
            chapter.introduction = data['introduction']
            chapter.conclusion = data['conclusion']
            chapter.save()
            return redirect(chapter.get_absolute_url())
    else:
        if chapter.part:
            form = ChapterForm({
                'title': chapter.title,
                'introduction': chapter.introduction,
                'conclusion': chapter.conclusion
            })
        else:
            form = EmbdedChapterForm({
                'introduction': chapter.introduction,
                'conclusion': chapter.conclusion
            })

    return render_template('tutorial/edit_chapter.html', {
        'chapter': chapter, 'form': form
    })


# Extract

@login_required
def add_extract(request):
    '''Add extract'''

    try:
        chapter_pk = int(request.GET['chapitre'])
    except KeyError:
        raise Http404
    chapter = get_object_or_404(Chapter, pk=chapter_pk)

    notify = None

    if request.method == 'POST':
        form = ExtractForm(request.POST)
        if form.is_valid():
            data = form.data
            extract = Extract()
            extract.chapter = chapter
            extract.position_in_chapter = chapter.get_extract_count() + 1
            extract.title = data['title']
            extract.text = data['text']
            extract.save()

            if 'submit_continue' in request.POST:
                form = ExtractForm()
                messages.success(
                    request, u'Extrait « {0} » ajouté avec succès.'.format(
                    extract.title))
            else:
                return redirect(extract.get_absolute_url())
    else:
        form = ExtractForm()

    return render_template('tutorial/new_extract.html', {
        'chapter': chapter, 'form': form, 'notify': notify
    })


@login_required
def edit_extract(request):
    '''Edit extract'''
    try:
        extract_pk = request.GET['extrait']
    except KeyError:
        raise Http404

    extract = get_object_or_404(Extract, pk=extract_pk)

    big = extract.chapter.part
    if big and (not request.user in extract.chapter.part.tutorial.authors.all())\
            or not big and (not request.user in
                            extract.chapter.tutorial.authors.all()):
        raise Http404

    if request.method == 'POST':
        form = EditExtractForm(request.POST)
        if form.is_valid():
            data = form.data
            extract.title = data['title']
            extract.text = data['text']
            extract.save()
            return redirect(extract.get_absolute_url())
    else:
        form = EditExtractForm({
            'title': extract.title,
            'text': extract.text
        })

    return render_template('tutorial/edit_extract.html', {
        'extract': extract, 'form': form
    })


def modify_extract(request):
    if not request.method == 'POST':
        raise Http404
    data = request.POST
    try:
        extract_pk = request.POST['extract']
    except KeyError:
        raise Http404

    extract = get_object_or_404(Extract, pk=extract_pk)
    chapter = extract.chapter

    if 'delete' in data:
        old_pos = extract.position_in_chapter
        for extract_c in extract.chapter.get_extracts():
            if old_pos <= extract_c.position_in_chapter:
                extract_c.position_in_chapter = extract_c.position_in_chapter - \
                    1
                extract_c.save()
        extract.delete()
        return redirect(chapter.get_absolute_url())

    elif 'move' in data:
        new_pos = int(request.POST['move_target'])
        move(extract, new_pos, 'position_in_chapter', 'chapter',
             'get_extracts')
        extract.save()

        return redirect(extract.get_absolute_url())

    raise Http404


# Handling deprecated links

def deprecated_view_tutorial_redirect(request, tutorial_pk, tutorial_slug):
    tutorial = get_object_or_404(Tutorial, pk=tutorial_pk)
    return redirect(tutorial.get_absolute_url(), permanent=True)


def deprecated_view_part_redirect(request, tutorial_pk, tutorial_slug, part_pos, part_slug):
    part = Part.objects.get(
        position_in_tutorial=part_pos, tutorial__pk=tutorial_pk)
    return redirect(part.get_absolute_url(), permanent=True)


def deprecated_view_chapter_redirect(
    request, tutorial_pk, tutorial_slug, part_pos, part_slug,
        chapter_pos, chapter_slug):
    chapter = Chapter.objects.get(position_in_part=chapter_pos,
                                  part__position_in_tutorial=part_pos,
                                  part__tutorial__pk=tutorial_pk)
    return redirect(chapter.get_absolute_url(), permanent=True)
