# coding: utf-8

from datetime import datetime

from django.shortcuts import get_object_or_404, redirect
from django.http import Http404, HttpResponse, HttpResponseBadRequest
from django.core.urlresolvers import reverse
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from pdp.utils import render_template, slugify, bot
from pdp.utils.cache import template_cache_delete
from pdp.utils.tutorials import move, export_tutorial
from pdp.settings import BOT_ENABLED

from .models import Tutorial, Part, Chapter, Extract
from .models import get_last_tutorials

from .forms import TutorialForm, EditTutorialForm, AddPartForm, EditPartForm, \
    AddChapterForm, EditChapterForm, EmbdedChapterForm, ExtractForm, \
    EditExtractForm


def index(request):
    """Display tutorials list.

    Returns:
        HttpResponse

    """
    tutorials = Tutorial.objects.all() \
        .filter(is_visible=True) \
        .order_by("-pubdate")

    pending_tutorials = None
    if request.user.has_perm('tutorial.change_tutorial'):
        pending_tutorials = Tutorial.objects.filter(is_pending=True)

    return render_template('tutorial/index.html', {
        'tutorials': tutorials,
        'pending_tutorials': pending_tutorials
    })


# Tutorial

def view_tutorial(request, tutorial_pk, tutorial_slug):
    """Display a tutorial.

    Returns:
        HttpResponse

    """
    tutorial = get_object_or_404(Tutorial, pk=tutorial_pk)

    if not tutorial.is_visible \
       and not request.user.has_perm('tutorial.change_tutorial') \
       and request.user not in tutorial.authors.all():
        if not (tutorial.is_beta and request.user.is_authenticated()):
            raise Http404

    # Make sure the URL is well-formed
    if not tutorial_slug == slugify(tutorial.title):
        return redirect(tutorial.get_absolute_url())

    # Two variables to handle two distinct cases (large/small tutorial)
    chapter = None
    parts = None
    part = None

    # If it's a small tutorial, fetch its chapter
    if tutorial.size == Tutorial.SMALL:
        chapter = Chapter.objects.get(tutorial=tutorial)
    elif tutorial.size == Tutorial.MEDIUM:
        part = Part.objects.get(tutorial=tutorial)
    else:
        parts = Part.objects.all(
        ).filter(tutorial=tutorial).order_by('position_in_tutorial')

    return render_template('tutorial/view_tutorial.html', {
        'tutorial': tutorial,
        'chapter': chapter,
        'part': part,
        'parts': parts,
    })


def download(request):
    """Download a tutorial.

    Returns:
        HttpResponse

    """
    import json

    tutorial_pk = request.GET.get('tutoriel', None)

    if tutorial_pk is None:
        return HttpResponseBadRequest()

    try:
        tutorial_pk = int(tutorial_pk)
    except ValueError:
        return HttpResponseBadRequest()

    tutorial = get_object_or_404(Tutorial, pk=tutorial_pk)

    if not tutorial.is_visible and not request.user in tutorial.authors.all():
        raise Http404

    dct = export_tutorial(tutorial, validate=False)
    data = json.dumps(dct, indent=4, ensure_ascii=False)

    response = HttpResponse(data, mimetype='application/json')
    response['Content-Disposition'] = 'attachment; filename={0}.json'\
        .format(tutorial.slug)

    return response


@login_required
def add_tutorial(request):
    """Add a tutorial.

    Returns:
        HttpResponse

    """
    if request.method == 'POST':
        form = TutorialForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.data
            # Creating a tutorial
            tutorial = Tutorial()
            tutorial.title = data['title']
            tutorial.description = data['description']
            tutorial.size = data['size']
            tutorial.pubdate = datetime.now()
            if 'image' in request.FILES:
                tutorial.image = request.FILES['image']
            tutorial.save()

            # We need to save the tutorial before changing its author list
            # since it's a many-to-many relationship
            tutorial.authors.add(request.user)
            # Save the icon
            if 'icon' in request.FILES:
                tutorial.icon = request.FILES['icon']
            tutorial.save()

            # If it's a small tutorial, create its corresponding chapter
            if tutorial.size == Tutorial.SMALL:
                chapter = Chapter()
                chapter.tutorial = tutorial
                chapter.save()

            # If it's a medium tutorial, create its corresponding part
            if tutorial.size == Tutorial.MEDIUM:
                part = Part()
                part.tutorial = tutorial
                part.save()

            return redirect(tutorial.get_absolute_url())
    else:
        form = TutorialForm()

    return render_template('tutorial/new_tutorial.html', {
        'form': form
    })


@login_required
def edit_tutorial(request):
    """Edit a tutorial.

    Returns:
        HttpResponse

    """
    try:
        tutorial_pk = request.GET['tutoriel']
    except KeyError:
        raise Http404

    tutorial = get_object_or_404(Tutorial, pk=tutorial_pk)

    if not request.user in tutorial.authors.all():
        raise Http404

    if request.method == 'POST':
        form = EditTutorialForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.data
            tutorial.title = data['title']
            tutorial.description = data['description']
            tutorial.introduction = data['introduction']
            tutorial.conclusion = data['conclusion']
            if 'image' in request.FILES:
                tutorial.image = request.FILES['image']
            tutorial.save()

            # If the tutorial was on the home page, clean cache
            if tutorial in get_last_tutorials():
                template_cache_delete('home-tutorials')

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


@require_POST
@login_required
def modify_tutorial(request):
    """Modify a tutorial.

    Returns:
        HttpResponse

    """

    tutorial_pk = request.POST['tutorial']
    tutorial = get_object_or_404(Tutorial, pk=tutorial_pk)

    # Validator actions
    if request.user.has_perm('tutorial.change_tutorial'):
        if 'validate' in request.POST:

            # We can't validate a non-pending tutorial
            if not tutorial.is_pending:
                raise PermissionDenied

            tutorial.is_pending = False
            tutorial.is_beta = False
            tutorial.is_visible = True
            tutorial.pubdate = datetime.now()
            tutorial.save()

            # We create a topic on forum for feedback
            if BOT_ENABLED:
                bot.create_tutorial_topic(tutorial)

            # We update home page tutorial cache
            template_cache_delete('home-tutorials')

            return redirect(tutorial.get_absolute_url())

        if 'refuse' in request.POST:
            if not tutorial.is_pending:
                raise PermissionDenied

            tutorial.is_pending = False
            tutorial.save()

            return redirect(tutorial.get_absolute_url())

    # User actions
    if request.user in tutorial.authors.all():
        if 'add_author' in request.POST:
            redirect_url = reverse('pdp.tutorial.views.edit_tutorial') + \
                '?tutoriel={0}'.format(tutorial.pk)

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
            redirect_url = reverse('pdp.tutorial.views.edit_tutorial') + \
                '?tutoriel={0}'.format(tutorial.pk)

            # Avoid orphan tutorials
            if tutorial.authors.all().count() <= 1:
                raise PermissionDenied

            author_pk = request.POST['author']
            author = get_object_or_404(User, pk=author_pk)

            tutorial.authors.remove(author)
            tutorial.save()

            return redirect(redirect_url)

        elif 'delete' in request.POST:
            tutorial.delete()
            return redirect('/tutoriels/')

        elif 'pending' in request.POST:
            if tutorial.is_pending:
                raise PermissionDenied

            tutorial.is_pending = True
            tutorial.save()
            return redirect(tutorial.get_absolute_url())

        elif 'beta' in request.POST:
            tutorial.is_beta = not tutorial.is_beta
            tutorial.save()
            return redirect(tutorial.get_absolute_url())

    # No action performed, no rights for request user, or not existing
    # action called.
    raise PermissionDenied


# Part

def view_part(request, tutorial_pk, tutorial_slug, part_slug):
    """Display a part.

    Returns:
        HttpResponse

    """
    part = get_object_or_404(Part,
                             slug=part_slug, tutorial__pk=tutorial_pk)

    tutorial = part.tutorial
    if not tutorial.is_visible \
       and not request.user.has_perm('tutorial.change_part') \
       and not request.user in tutorial.authors.all():
        if not (tutorial.is_beta and request.user.is_authenticated()):
            raise PermissionDenied

    # Make sure the URL is well-formed
    if not tutorial_slug == slugify(tutorial.title)\
            or not part_slug == slugify(part.title):
        return redirect(part.get_absolute_url())

    return render_template('tutorial/view_part.html', {
        'part': part
    })


@login_required
def add_part(request):
    """Add a new part.

    Returns:
        HttpResponse

    """
    try:
        tutorial_pk = request.GET['tutoriel']
    except KeyError:
        raise Http404

    # TODO: do not show error about empty title on new form

    tutorial = get_object_or_404(Tutorial, pk=tutorial_pk)
    # Make sure it's a big tutorial, just in case
    if not tutorial.size == Tutorial.BIG:
        raise PermissionDenied
    # Make sure the user belongs to the author list
    if not request.user in tutorial.authors.all():
        raise PermissionDenied
    if request.method == 'POST':
        form = AddPartForm(request.POST)
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
        form = AddPartForm({'tutorial': tutorial.pk})
    return render_template('tutorial/new_part.html', {
        'tutorial': tutorial, 'form': form
    })


@require_POST
@login_required
def modify_part(request):
    """Modifiy a part.

    Returns:
        HttpResponse

    """
    part_pk = request.POST['part']
    part = get_object_or_404(Part, pk=part_pk)

    # Make sure the user is allowed to do that
    if not request.user in part.tutorial.authors.all():
        raise PermissionDenied

    if 'move' in request.POST:
        try:
            new_pos = int(request.POST['move_target'])
        # Invalid conversion, maybe the user played with the move button
        except ValueError:
            return redirect(part.tutorial.get_absolute_url())

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
    """Edit a part.

    Returns:
        HttpResponse

    """
    try:
        part_pk = int(request.GET['partie'])
    except KeyError:
        raise Http404
    part = get_object_or_404(Part, pk=part_pk)
    # Make sure the user is allowed to do that
    if not request.user in part.tutorial.authors.all():
        raise PermissionDenied

    if request.method == 'POST':
        form = EditPartForm(request.POST)
        if form.is_valid():
            data = form.data
            part.title = data['title']
            part.introduction = data['introduction']
            part.conclusion = data['conclusion']
            part.save()
            return redirect(part.get_absolute_url())
    else:
        form = EditPartForm({
            'title': part.title,
            'introduction': part.introduction,
            'conclusion': part.conclusion,
            'tutorial': part.tutorial.pk,
            'part': part.pk
        })

    return render_template('tutorial/edit_part.html', {
        'part': part, 'form': form
    })


# Chapter

def view_chapter(request, tutorial_pk, tutorial_slug, part_slug,
                 chapter_slug):
    """Display a chapter.

    Returns:
        HttpResponse

    """

    chapter = get_object_or_404(Chapter,
                                slug=chapter_slug,
                                part__slug=part_slug,
                                part__tutorial__pk=tutorial_pk)

    tutorial = chapter.get_tutorial()
    if not tutorial.is_visible \
       and not request.user.has_perm('tutorial.modify_chapter') \
       and not request.user in tutorial.authors.all():
        if not (tutorial.is_beta and request.user.is_authenticated()):
            raise PermissionDenied

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
    """Add a new chapter to a part.

    Returns:
        HttpResponse

    """
    try:
        part_pk = request.GET['partie']
    except KeyError:
        raise Http404
    part = get_object_or_404(Part, pk=part_pk)

    # TODO: do not show error about empty title on new form

    # Make sure the user is allowed to do that
    if not request.user in part.tutorial.authors.all():
        raise PermissionDenied

    if request.method == 'POST':
        form = AddChapterForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.data

            chapter = Chapter()
            chapter.title = data['title']
            chapter.introduction = data['introduction']
            chapter.conclusion = data['conclusion']
            chapter.part = part
            chapter.position_in_part = part.get_chapters().count() + 1
            chapter.update_position_in_tutorial()
            if 'image' in request.FILES:
                chapter.image = request.FILES['image']
            chapter.save()

            if 'submit_continue' in request.POST:
                form = AddChapterForm({'part': part.pk})
                messages.success(request,
                                 u'Chapitre « {0} » ajouté avec succès.'
                                 .format(chapter.title))
            else:
                return redirect(chapter.get_absolute_url())
    else:
        form = AddChapterForm({'part': part.pk})

    return render_template('tutorial/new_chapter.html', {
        'part': part, 'form': form
    })


@require_POST
@login_required
def modify_chapter(request):
    """Modify a chapter.

    Returns:
        HttpResponse

    """
    data = request.POST

    try:
        chapter_pk = request.POST['chapter']
    except KeyError:
        raise Http404

    chapter = get_object_or_404(Chapter, pk=chapter_pk)

    # Make sure the user is allowed to do that
    if not request.user in chapter.get_tutorial().authors.all():
        raise PermissionDenied

    if 'move' in data:
        try:
            new_pos = int(request.POST['move_target'])
        # User misplayed with the move button
        except ValueError:
            return redirect(chapter.get_absolute_url())

        move(chapter, new_pos, 'position_in_part', 'part', 'get_chapters')
        chapter.update_position_in_tutorial()
        chapter.save()

        messages.info(request, u'Le chapitre a bien été déplacé.')

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

        messages.info(request, u'Le chapitre a bien été supprimé.')

        return redirect(chapter.part.get_absolute_url())

    return redirect(chapter.get_absolute_url())


@login_required
def edit_chapter(request):
    """Edit a chapter.

    Returns:
        HttpResponse

    """

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
        raise PermissionDenied

    if request.method == 'POST':

        if chapter.part:
            form = EditChapterForm(request.POST, request.FILES)
        else:
            form = EmbdedChapterForm(request.POST, request.FILES)

        if form.is_valid():
            data = form.data
            if chapter.part:
                chapter.title = data['title']
            chapter.introduction = data['introduction']
            chapter.conclusion = data['conclusion']
            if 'image' in request.FILES:
                    chapter.image = request.FILES['image']
            chapter.save()
            return redirect(chapter.get_absolute_url())
    else:
        if chapter.part:
            form = EditChapterForm({
                'title': chapter.title,
                'introduction': chapter.introduction,
                'conclusion': chapter.conclusion,
                'part': chapter.part.pk,
                'chapter': chapter.pk
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
    """Add an extract.

    Returns:
        HttpResponse

    """

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
                    request, u'Extrait « {0} » ajouté avec succès.'
                    .format(extract.title))
            else:
                return redirect(extract.get_absolute_url())
    else:
        form = ExtractForm()

    return render_template('tutorial/new_extract.html', {
        'chapter': chapter, 'form': form, 'notify': notify
    })


@login_required
def edit_extract(request):
    """Edit an extract.

    Returns:
        HttpResponse

    """

    try:
        extract_pk = request.GET['extrait']
    except KeyError:
        raise Http404

    extract = get_object_or_404(Extract, pk=extract_pk)

    b = extract.chapter.part
    if b and (not request.user in extract.chapter.part.tutorial.authors.all())\
            or not b and (not request.user in
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


@require_POST
@login_required
def modify_extract(request):
    """Modify an extract.

    Returns:
        HttpResponse

    """
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
                extract_c.position_in_chapter = extract_c.position_in_chapter \
                    - 1
                extract_c.save()
        extract.delete()
        return redirect(chapter.get_absolute_url())

    elif 'move' in data:
        try:
            new_pos = int(request.POST['move_target'])
        # Error, the user misplayed with the move button
        except ValueError:
            return redirect(extract.get_absolute_url())

        move(extract, new_pos, 'position_in_chapter', 'chapter',
             'get_extracts')
        extract.save()

        return redirect(extract.get_absolute_url())

    raise PermissionDenied


def find_tutorial(request, name):
    """Find all tutorials written by an user.

    Returns:
        HttpResponse

    """
    u = get_object_or_404(User, username=name)

    tutos = Tutorial.objects.all()\
        .filter(authors__in=[u])\
        .filter(is_visible=True)\
        .order_by('-pubdate')

    return render_template('tutorial/find_tutorial.html', {
        'tutos': tutos, 'usr': u,
    })
