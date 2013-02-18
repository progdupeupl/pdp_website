# coding: utf-8

from django.shortcuts import get_object_or_404, redirect
from django.http import Http404

from pdp.utils import render_template, slugify

from .models import Tutorial, Part, Chapter, Extract
from .forms import TutorialForm, PartForm, ChapterForm, ExtractForm

def index(request):
    t = Tutorial.objects.all().filter(is_visible=True)

    if request.user.is_authenticated():
        user_t = Tutorial.objects.filter(authors=request.user)
    else:
        user_t = None

    return render_template('tutorial/index.html', {
        'tutorials': t,
        'user_tutorials': user_t
    })


def view_tutorial(request, tutorial_pk, tutorial_slug):

    t = get_object_or_404(Tutorial, pk=tutorial_pk)

    if not t.is_visible and request.user not in t.authors.all():
        raise Http404

    # On vérifie que l'URL est correcte
    if not tutorial_slug == slugify(t.title):
        return redirect(t.get_absolute_url())

    # On prévoit deux variables pour gérer les deux cas de figure
    c = None
    p = None

    # Si le tuto est un mini-tuto, alors on va chercher le chapitre
    # correspondant
    if t.is_mini:
        c = Chapter.objects.get(tutorial=t)
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

            # Création du tutoriel
            t = Tutorial()
            t.title = data['title']
            t.description = data['description']
            t.is_mini = 'is_mini' in data
            t.save()

            # On doit sauvegarder obligatoirement le tutoriel avant d'être
            # autorisé à modifier la liste des auteurs (many-to-many)
            t.authors.add(request.user)

            # On sauvegarde l'icone
            if 'icon' in request.FILES:
                t.icon = request.FILES['icon']

            t.save()

            # S'il s'agit d'un mini-tuto, on lui attribue un chapitre d'office
            if t.is_mini:
                c = Chapter()
                c.tutorial = t
                c.save()

            return redirect(t.get_absolute_url())

        else:
            # TODO: retourner la form avec les erreurs
            raise Http404

    else:
        return render_template('tutorial/new_tutorial.html')


def view_chapter(request, tutorial_pk, tutorial_slug, part_pos, part_slug, chapter_pos, chapter_slug):

    c = Chapter.objects.get(position_in_part=chapter_pos, part__position_in_tutorial=part_pos, part__tutorial__pk=tutorial_pk)

    if not c.get_tutorial().is_visible and not request.user in c.get_tutorial().authors.all():
        raise Http404

    # On vérifie que l'URL est correcte
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

    # On vérifie que l'URL est correcte
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

    # On s'assure qu'il s'agit bien d'un big-tuto
    if t.is_mini:
        raise Http404

    # On vérifie que l'utilisateur fait partie des auteurs
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
            # TODO: retourner le formulaire avec les erreurs
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

    # On vérifie que l'utilisateur a le doit de faire ça
    if not request.user in p.tutorial.authors.all():
        raise Http404

    if 'move' in request.POST:
        new_pos = int(request.POST['move_target'])
        old_pos = p.position_in_tutorial

        # On vérifie que la position n'est pas incorrecte
        if new_pos < 1 or new_pos > p.tutorial.get_parts().count():
            raise ValueError('La nouvelle position demandée est incorrecte')

        # On met à jour les autres parties en changeant également leur position
        # Faire un schéma sur papier pour comprendre l'algo pourrait vous aider
        # si vous êtes curieux de savoir comment ça fonctionne
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

        # On sauvegarde la nouvelle position une fois que le reste a été rangé
        p.position_in_tutorial = new_pos
        p.save()

    elif 'delete' in request.POST:
        # On supprime tous les chapitres associés à la partie
        Chapter.objects.all().filter(part=p).delete()

        # On réagence les autres parties du tutoriel
        old_pos = p.position_in_tutorial
        for tut_p in p.tutorial.get_parts():
            if old_pos <= tut_p.position_in_tutorial:
                tut_p.position_in_tutorial = tut_p.position_in_tutorial - 1
                tut_p.save()

        # Enfin, on supprime à proprement parler la partie
        p.delete()

    return redirect(p.tutorial.get_absolute_url())


def edit_part(request):
    try:
        part_pk = int(request.GET['partie'])
    except KeyError:
        raise Http404

    p = get_object_or_404(Part, pk=part_pk)

    # On vérifie que l'utilisateur a bien le droit de faire ça
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

    # On vérifie que l'utilisateur a le droit de faire ça
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

    # On vérifie que l'utilisateur a le doit de faire ça
    #if not request.user in c.part.tutorial.authors.all():
    #   raise Http404

    if 'move' in data:
        new_pos = int(request.GET['position'])
        old_pos = c.position_in_part

        # On vérifie que la position n'est pas incorrecte
        if new_pos < 1 or new_pos > c.part.get_chapters().count():
            raise ValueError('La nouvelle position demandée est incorrecte')

        # On met à jour les autres parties en changeant également leur position
        # Faire un schéma sur papier pour comprendre l'algo pourrait vous aider
        # si vous êtes curieux de savoir comment ça fonctionne
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

        # On sauvegarde la nouvelle position une fois que le reste a été rangé
        c.position_in_part = new_pos
        c.save()

    elif 'delete' in data:

        # On réagence les autres parties du tutoriel
        old_pos = c.position_in_part
        for tut_c in c.part.get_chapters():
            if old_pos <= tut_c.position_in_part:
                tut_c.position_in_part = tut_c.position_in_part - 1
                tut_c.save()

        # Enfin, on supprime à proprement parler la partie
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

    # On vérifie que l'utilisateur a bien le droit de faire ça
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