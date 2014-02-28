# coding: utf-8

"""A small module for handling some common operations on tutorials."""

from collections import OrderedDict
from itertools import repeat
import subprocess

from pdp.tutorial.models import Tutorial, Part, Chapter, Extract
from pdp.utils.schemas import validate_tutorial


def move(obj, new_pos, position_f, parent_f, children_fn):
    """Move an object and reorder other objects affected by moving.

    This function need the object, the new position you want the object to go,
    the position field name of the object (eg. 'position_in_chapter'), the
    parent field of the object (eg. 'chapter') and the children function's
    name to apply to parent (eg. 'get_extracts').

    You will still have to save the object once modified.

    Example for extracts :

      move(extract, new_pos, 'position_in_chapter', 'chapter', 'get_extracts')

    """
    old_pos = getattr(obj, position_f)
    objects = getattr(getattr(obj, parent_f), children_fn)()

    # Check that asked new position is correct
    if not 1 <= new_pos <= objects.count():
        raise ValueError('Can\'t move object to position {0}'.format(new_pos))

    increased_pos = new_pos - old_pos > 0

    # Loop on other extracts to move them first
    for obj_mv in objects:
        # If position was increased and obj was between older and new position,
        # lower their position by one
        if increased_pos \
                and old_pos <= getattr(obj_mv, position_f) <= new_pos:
            setattr(obj_mv, position_f, getattr(obj_mv, position_f) - 1)
            obj_mv.save()
        # Otherwise if position was decreased and obj was between newer and old
        # position, increase their position by one
        elif not increased_pos \
                and new_pos <= getattr(obj_mv, position_f) <= old_pos:
            setattr(obj_mv, position_f, getattr(obj_mv, position_f) + 1)
            obj_mv.save()

    # All objects have been updated except the current one we want to move, so
    # we can do it now
    setattr(obj, position_f, new_pos)


# Export-to-dict functions

def export_chapter(chapter, export_all=True):
    """Export a chapter to a dict.

    Args:
        chapter: The chapter database model to export

    Returns:
        A dictionnary containing extract data.

    """
    dct = OrderedDict()
    if export_all:
        dct['title'] = chapter.title
        dct['introduction'] = chapter.introduction
        dct['conclusion'] = chapter.conclusion
    dct['extracts'] = []

    extracts = Extract.objects.filter(chapter=chapter)\
        .order_by('position_in_chapter')

    for extract in extracts:
        extract_dct = OrderedDict()
        extract_dct['title'] = extract.title
        extract_dct['text'] = extract.text
        dct['extracts'].append(extract_dct)

    return dct


def export_part(part):
    """Export a part to a dict.

    Args:
        part: The part database model to export

    Returns:
        A dictionnary containing part data.

    """
    dct = OrderedDict()
    dct['title'] = part.title
    dct['introduction'] = part.introduction
    dct['conclusion'] = part.conclusion
    dct['chapters'] = []

    chapters = Chapter.objects\
        .filter(part=part)\
        .order_by('position_in_part')
    for chapter in chapters:
        dct['chapters'].append(export_chapter(chapter))

    return dct


def export_tutorial(tutorial, validate=True):
    """Export a tutorial to a dict.

    Args:
        tutorial: The tutorial database model to export
        validate: Should the output dictionnary be checked?

    Returns:
        A dictionnary containing tutorial data. If the validate option is set
        and the validation fails, it will fail silently returning an empty
        dictionnary instead.

    """

    dct = OrderedDict()
    dct['title'] = tutorial.title
    dct['description'] = tutorial.description
    dct['is_mini'] = tutorial.size == Tutorial.SMALL
    dct['authors'] = [a.username for a in tutorial.authors.all()]
    dct['introduction'] = tutorial.introduction
    dct['conclusion'] = tutorial.conclusion

    if tutorial.size == Tutorial.SMALL:
        # We export the chapter without its empty title if small tutorial
        chapter = Chapter.objects.get(tutorial=tutorial)
        dct['chapter'] = export_chapter(chapter, export_all=False)
    else:
        dct['parts'] = []
        parts = Part.objects\
            .filter(tutorial=tutorial)\
            .order_by('position_in_tutorial')
        for part in parts:
            dct['parts'].append(export_part(part))

    # If validation is requested and fails, just return empty dict
    if validate and not validate_tutorial(dct):
        return {}

    return dct

# Export-to-PDF functions using Pandoc


def export_title_md(f, title, level=1):
    f.write('{} {}\n'.format(
        ''.join(repeat('#', level)),
        title,
    ))


def export_text_md(f, text):
    f.write(text)
    f.write('\n\n')


def export_extract_md(f, extract, level=1):
    export_title_md(f, extract.title, level)
    export_text_md(f, extract.text)


def export_chapter_md(f, chapter, level=1, export_all=True):
    if export_all:
        export_title_md(f, chapter.title, level)
        export_text_md(f, chapter.introduction)

    for extract in chapter.get_extracts():
        export_extract_md(f, extract, level + 1 if export_all else level)

    if export_all:
        export_text_md(f, chapter.conclusion)


def export_part_md(f, part, level=1, export_all=True):
    if export_all:
        export_title_md(f, part.title, level)
        export_text_md(f, part.introduction)

    for chapter in part.get_chapters():
        export_chapter_md(f, chapter, level + 1 if export_all else level)

    if export_all:
        export_text_md(f, part.conclusion)


def export_tutorial_pdf(tutorial):
    title = tutorial.title
    authors = u'; '.join([a.username for a in list(tutorial.authors.all())])

    md_filepath = '/tmp/test.md'
    pdf_filepath = '/tmp/test.pdf'

    with open(md_filepath, 'w') as f:
        f.write('% {}\n'.format(title))
        f.write('% {}\n'.format(authors))

        f.write('\n\n')

        export_text_md(f, tutorial.introduction)

        if tutorial.size == Tutorial.BIG:
            for part in tutorial.get_parts():
                export_part_md(f, part)

        elif tutorial.size == Tutorial.MEDIUM:
            export_part_md(f, tutorial.get_parts()[0], export_all=False)

        elif tutorial.size == Tutorial.SMALL:
            export_chapter(f, tutorial.get_chapter(), export_all=False)

        export_text_md(f, tutorial.conclusion)

    subprocess.call(['pandoc', '-N', '-o', pdf_filepath, md_filepath])
