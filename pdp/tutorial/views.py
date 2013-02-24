# coding: utf-8

from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

from pdp.utils import render_template, slugify

from .models import Tutorial, Part, Chapter, Extract
from .forms import *


def index(request):
    '''Display tutorials list'''
    tutorials = Tutorial.objects.all().filter(is_visible=True)

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
            raise Http404
    else:
        form = TutorialForm()

    return render_template('tutorial/new_tutorial.html', {
        'form': form
    })


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
            tutorial.save()
            return redirect(t.get_absolute_url())
    else:
        form = EditTutorialForm({
            'title': tutorial.title,
            'description': tutorial.description
        })

    return render_template('tutorial/edit_tutorial.html', {
        'tutorial': tutorial, 'form': form
    })

# Part


def view_part(request, tutorial_pk, tutorial_slug, part_pos, part_slug):
    '''Display a part'''
    part = Part.objects.get(
        position_in_tutorial=part_pos, tutorial__pk=tutorial_pk)

    if not part.tutorial.is_visible and not request.user in \
            part.tutorial.authors.all():
        raise Http404

    # Make sure the URL is well-formed
    if not tutorial_slug == slugify(part.tutorial.title)\
            or not part_slug == slugify(part.title):
        return redirect(part.get_absolute_url())

    return render_template('tutorial/view_part.html', {
        'part': part
    })


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
        'tutorial': t, 'form': form
    })


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
        old_pos = part.position_in_tutorial

        # Make sure the requested position is correct
        if new_pos < 1 or new_pos > part.tutorial.get_parts().count():
            raise ValueError('La nouvelle position demandée est incorrecte')

        # Update other parts by changing their position
        # Draw a schema on a piece of paper
        #     if you want to understand how this works
        # TODO: if the above comment is needed,
        #     there's probably a better algorithm
        pos_increased = new_pos - old_pos > 0
        for tut_p in part.tutorial.get_parts():
            if pos_increased \
                    and old_pos <= tut_p.position_in_tutorial <= new_pos:
                tut_p.position_in_tutorial = tut_p.position_in_tutorial - 1
                tut_p.save()
            elif not pos_increased \
                    and new_pos <= tut_p.position_in_tutorial <= old_pos:
                tut_p.position_in_tutorial = tut_p.position_in_tutorial + 1
                tut_p.save()

        # Save the new position after the other parts have been sorted
        part.position_in_tutorial = new_pos
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

def view_chapter(request, tutorial_pk, tutorial_slug, part_pos, part_slug,
                 chapter_pos, chapter_slug):
    '''View chapter'''

    chapter = Chapter.objects.get(position_in_part=chapter_pos,
                                  part__position_in_tutorial=part_pos,
                                  part__tutorial__pk=tutorial_pk)

    if not chapter.get_tutorial().is_visible \
            and not request.user in chapter.get_tutorial().authors.all():
        raise Http404

    if not tutorial_slug == slugify(chapter.part.tutorial.title)\
        or not part_slug == slugify(chapter.part.title)\
            or not chapter_slug == slugify(chapter.title):
        return redirect(chapter.get_absolute_url())

    return render_template('tutorial/view_chapter.html', {
        'chapter': chapter
    })


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
            chapter = Chapter()
            chapter.title = data['title']
            chapter.introduction = data['introduction']
            chapter.conclusion = data['conclusion']
            chapter.part = part
            chapter.position_in_part = part.get_chapters().count() + 1
            chapter.save()
            return redirect(chapter.get_absolute_url())
    else:
        form = ChapterForm()

    return render_template('tutorial/new_chapter.html', {
        'part': part, 'form': form
    })


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
    #if not request.user in c.part.tutorial.authors.all():
    #   raise Http404

    if 'move' in data:
        new_pos = int(request.GET['position'])
        old_pos = chapter.position_in_part

        # Make sure the requested position is valid
        if new_pos < 1 or new_pos > chapter.part.get_chapters().count():
            raise ValueError('La nouvelle position demandée est incorrecte')

        # Update other chapters by changing their position
        # Draw a schema on a piece of paper if you want to understand how this works
        # TODO: if the above comment is needed,
        #       there's probably a better algorithm
        pos_increased = new_pos - old_pos > 0
        for tut_c in chapter.part.get_chapters():
            if pos_increased \
                    and old_pos <= tut_c.position_in_part <= new_pos:
                tut_c.position_in_part = tut_c.position_in_part - 1
                tut_c.save()
            elif not pos_increased \
                    and new_pos <= tut_c.position_in_part <= old_pos:
                tut_c.position_in_part = tut_c.position_in_part + 1
                tut_c.save()
        # Save the new position once other chapters have been sorted
        chapter.position_in_part = new_pos
        chapter.save()
    elif 'delete' in data:
        # Move other chapters first
        old_pos = chapter.position_in_part
        for tut_c in chapter.part.get_chapters():
            if old_pos <= tut_c.position_in_part:
                tut_c.position_in_part = tut_c.position_in_part - 1
                tut_c.save()
        # Then delete the chapter
        chapter.delete()

    return redirect(chapter.part.tutorial.get_absolute_url())


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

def add_extract(request):
    '''Add extract'''

    try:
        chapter_pk = int(request.GET['chapitre'])
    except KeyError:
        raise Http404
    chapter = get_object_or_404(Chapter, pk=chapter_pk)

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
            return redirect(extract.get_absolute_url())
    else:
        form = ExtractForm()

    return render_template('tutorial/new_extract.html', {
        'chapter': chapter, 'form': form
    })


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
        form = ExtractForm(request.POST)
        if form.is_valid():
            data = form.data
            extract.title = data['title']
            extract.text = data['text']
            extract.save()
            return redirect(extract.get_absolute_url())
    else:
        form = ExtractForm({
            'title': extract.title,
            'text': extract.text
        })

    return render_template('tutorial/edit_extract.html', {
        'extract': extract, 'form': form
    })
