# coding: utf-8

from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

from pdp.utils import render_template, slugify

from .models import Tutorial, Part, Chapter, Extract
from .forms import TutorialForm, PartForm, ChapterForm, ExtractForm

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


def view_tutorial(request, tutorial_pk, tutorial_slug):
    '''Display a tutorial'''
    tutorial = get_object_or_404(Tutorial, pk=tutorial_pk)

    if not tutorial.is_visible and request.user not in tutorial.authors.all():
        raise Http404

    # Make sure the URL is well-formed
    if not tutorial_slug == slugify(tutorial.title):
        return redirect(tutorial.get_absolute_url())

    # Two variables to handle two distinct cases (large/small tutorial)
    c = None
    p = None

    # If it's a small tutorial, fetch its chapter
    if tutorial.is_mini:
        c = Chapter.objects.get(tutorial=tutorial)
    else:
        p = Part.objects.all(
        ).filter(tutorial=t).order_by('position_in_tutorial')

    return render_template('tutorial/view_tutorial.html', {
        'tutorial': t, 'chapter': c, 'parts': p
    })


def add_tutorial(request):

    if request.method == 'POST':
        form = TutorialForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.data

            # Creating a tutorial
            t = Tutorial()
            t.title = data['title']
            t.description = data['description']
            t.is_mini = 'is_mini' in data
            t.save()

            # We need to save the tutorial before changing its author list
            # since it's a many-to-many relationship
            t.authors.add(request.user)

            # Save the icon
            if 'icon' in request.FILES:
                t.icon = request.FILES['icon']

            t.save()

            # If it's a small tutorial, create its corresponding chapter
            if t.is_mini:
                c = Chapter()
                c.tutorial = t
                c.save()

            return redirect(t.get_absolute_url())

        else:
            # TODO: add errors to the form and return it
            raise Http404

    else:
        return render_template('tutorial/new_tutorial.html')


def view_chapter(request, tutorial_pk, tutorial_slug, part_pos, part_slug, chapter_pos, chapter_slug):

    c = Chapter.objects.get(position_in_part=chapter_pos, part__position_in_tutorial=part_pos, part__tutorial__pk=tutorial_pk)

    if not c.get_tutorial().is_visible and not request.user in c.get_tutorial().authors.all():
        raise Http404

    # Make sure the URL is well-formed
    if not tutorial_slug == slugify(c.part.tutorial.title)\
        or not part_slug == slugify(c.part.title)\
            or not chapter_slug == slugify(c.title):
        return redirect(c.get_absolute_url())

    return render_template('tutorial/view_chapter.html', {
        'chapter': c
    })


def view_part(request, tutorial_pk, tutorial_slug, part_pos, part_slug):

    p = Part.objects.get(
        position_in_tutorial=part_pos, tutorial__pk=tutorial_pk)

    if not p.tutorial.is_visible and not request.user in p.tutorial.authors.all():
        raise Http404

    # Make sure the URL is well-formed
    if not tutorial_slug == slugify(p.tutorial.title)\
            or not part_slug == slugify(p.title):
        return redirect(p.get_absolute_url())

    return render_template('tutorial/view_part.html', {
        'part': p
    })


def add_part(request):

    try:
        tutorial_pk = request.GET['tutoriel']
    except KeyError:
        raise Http404

    t = get_object_or_404(Tutorial, pk=tutorial_pk)

    # Make sure it's a big tutorial, just in case
    if t.is_mini:
        raise Http404

    # Make sure the user belongs to the author list
    if not request.user in t.authors.all():
        raise Http404

    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            data = form.data

            p = Part()
            p.tutorial = t
            p.title = data['title']
            p.introduction = data['introduction']
            p.conclusion = data['conclusion']
            p.position_in_tutorial = t.get_parts().count() + 1

            p.save()

            return redirect(p.get_absolute_url())

        else:
            # TODO: add errors to the form and return it
            raise Http404
    else:
        return render_template('tutorial/new_part.html', {
            'tutorial': t
        })


def modify_part(request):
    if not request.method == 'POST':
        raise Http404

    part_pk = request.POST['part']
    p = get_object_or_404(Part, pk=part_pk)

    # Make sure the user is allowed to do that
    if not request.user in p.tutorial.authors.all():
        raise Http404

    if 'move' in request.POST:
        new_pos = int(request.POST['move_target'])
        old_pos = p.position_in_tutorial

        # Make sure the requested position is correct
        if new_pos < 1 or new_pos > p.tutorial.get_parts().count():
            raise ValueError('La nouvelle position demandée est incorrecte')

        # Update other parts by changing their position
        # Draw a schema on a piece of paper if you want to understand how this works
        # TODO: if the above comment is needed, there's probably a better algorithm
        pos_increased = new_pos - old_pos > 0
        for tut_p in p.tutorial.get_parts():
            if pos_increased \
                    and old_pos <= tut_p.position_in_tutorial <= new_pos:
                tut_p.position_in_tutorial = tut_p.position_in_tutorial - 1
                tut_p.save()
            elif not pos_increased \
                    and new_pos <= tut_p.position_in_tutorial <= old_pos:
                tut_p.position_in_tutorial = tut_p.position_in_tutorial + 1
                tut_p.save()

        # Save the new position after the other parts have been sorted
        p.position_in_tutorial = new_pos
        p.save()

    elif 'delete' in request.POST:
        # Delete all chapters belonging to the part
        Chapter.objects.all().filter(part=p).delete()

        # Move other parts
        old_pos = p.position_in_tutorial
        for tut_p in p.tutorial.get_parts():
            if old_pos <= tut_p.position_in_tutorial:
                tut_p.position_in_tutorial = tut_p.position_in_tutorial - 1
                tut_p.save()

        # Actually delete the part
        p.delete()

    return redirect(p.tutorial.get_absolute_url())


def edit_part(request):
    try:
        part_pk = int(request.GET['partie'])
    except KeyError:
        raise Http404

    p = get_object_or_404(Part, pk=part_pk)

    # Make sure the user is allowed to do that
    if not request.user in p.tutorial.authors.all():
        raise Http404

    if request.method == 'POST':
        form = PartForm(request.POST)
        if form.is_valid():
            data = form.data

            p.title = data['title']
            p.introduction = data['introduction']
            p.conclusion = data['conclusion']

            p.save()

            return redirect(p.get_absolute_url())
        else:
            raise Http404

    else:
        return render_template('tutorial/edit_part.html', {
            'part': p
        })


def add_chapter(request):
    try:
        part_pk = request.GET['partie']
    except KeyError:
        raise Http404

    p = get_object_or_404(Part, pk=part_pk)

    # Make sure the user is allowed to do that
    if not request.user in p.tutorial.authors.all():
        raise Http404

    if request.method == 'POST':
        form = ChapterForm(request.POST)
        if form.is_valid():
            data = form.data

            c = Chapter()
            c.title = data['title']
            c.introduction = data['introduction']
            c.conclusion = data['conclusion']
            c.part = p
            c.position_in_part = p.get_chapters().count() + 1
            c.save()

            return redirect(c.get_absolute_url())

        else:
            raise Http404

    else:
        return render_template('tutorial/new_chapter.html', {
            'part': p
        })


def modify_chapter(request):
    if not request.method == 'POST':
        raise Http404

    data = request.POST

    try:
        chapter_pk = request.POST['chapter']
    except KeyError:
        raise Http404

    c = get_object_or_404(Chapter, pk=chapter_pk)

    # Make sure the user is allowed to do that
    #if not request.user in c.part.tutorial.authors.all():
    #   raise Http404

    if 'move' in data:
        new_pos = int(request.GET['position'])
        old_pos = c.position_in_part

        # Make sure the requested position is valid
        if new_pos < 1 or new_pos > c.part.get_chapters().count():
            raise ValueError('La nouvelle position demandée est incorrecte')

        # Update other chapters by changing their position
        # Draw a schema on a piece of paper if you want to understand how this works
        # TODO: if the above comment is needed, there's probably a better algorithm
        pos_increased = new_pos - old_pos > 0
        for tut_c in c.part.get_chapters():
            if pos_increased \
                    and old_pos <= tut_c.position_in_part <= new_pos:
                tut_c.position_in_part = tut_c.position_in_part - 1
                tut_c.save()
            elif not pos_increased \
                    and new_pos <= tut_c.position_in_part <= old_pos:
                tut_c.position_in_part = tut_c.position_in_part + 1
                tut_c.save()

        # Save the new position once other chapters have been sorted
        c.position_in_part = new_pos
        c.save()

    elif 'delete' in data:
        # Move other chapters first
        old_pos = c.position_in_part
        for tut_c in c.part.get_chapters():
            if old_pos <= tut_c.position_in_part:
                tut_c.position_in_part = tut_c.position_in_part - 1
                tut_c.save()

        # Then delete the chapter
        c.delete()

    return redirect(c.part.tutorial.get_absolute_url())


def edit_chapter(request):
    try:
        chapter_pk = int(request.GET['chapitre'])
    except KeyError:
        raise Http404

    c = get_object_or_404(Chapter, pk=chapter_pk)
    big = c.part
    small = c.tutorial

    # Make sure the user is allowed to do that
    if big and (not request.user in c.part.tutorial.authors.all())\
            or small and (not request.user in c.tutorial.authors.all()):
        raise Http404

    if request.method == 'POST':
        form = ChapterForm(request.POST)

        if form.is_valid():
            data = form.data

            if c.part:
                c.title = data['title']
            else:
                t = c.tutorial
                t.title = data['title']
                t.description = data['description']
                t.save()

            c.introduction = data['introduction']
            c.conclusion = data['conclusion']

            c.save()

            return redirect(c.get_absolute_url())
        else:
            raise Http404
    else:
        return render_template('tutorial/edit_chapter.html', {
            'chapter': c
        })


def add_extract(request):
    try:
        chapter_pk = int(request.GET['chapitre'])
    except KeyError:
        raise Http404

    c = get_object_or_404(Chapter, pk=chapter_pk)

    if request.method == 'POST':
        form = ExtractForm(request.POST)

        if form.is_valid():
            data = form.data

            e = Extract()
            e.chapter = c
            e.position_in_chapter = c.get_extract_count() + 1
            e.title = data['title']
            e.text = data['text']
            e.save()

            return redirect(e.get_absolute_url())
        else:
            raise Http404
    else:
        return render_template('tutorial/new_extract.html', {
            'chapter': c
        })


def edit_extract(request):
    try:
        extract_pk = request.GET['extrait']
    except KeyError:
        raise Http404

    e = get_object_or_404(Extract, pk=extract_pk)

    big = e.chapter.part
    if big and (not request.user in e.chapter.part.tutorial.authors.all())\
            or not big and (not request.user in e.chapter.tutorial.authors.all()):
        raise Http404

    if request.method == 'POST':
        form = ExtractForm(request.POST)
        if form.is_valid():
            data = form.data

            e.title = data['title']
            e.text = data['text']
            e.save()

            return redirect(e.get_absolute_url())
    else:
        return render_template('tutorial/edit_extract.html', {
            'extract': e
        })
