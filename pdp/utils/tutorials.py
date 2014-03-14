# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

"""A small module for handling some common operations on tutorials."""

from collections import OrderedDict
from itertools import repeat

import os
import io
from datetime import datetime

from pdp import settings

from pdp.tutorial.models import Tutorial, Part, Chapter, Extract
from pdp.utils.schemas import validate_tutorial
from pdp.utils.tasks import pandoc_pdf


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

def size_to_string(size):
    """Return a string representing the tutorial size, used for export."""
    if size == Tutorial.SMALL:
        return u'small'
    elif size == Tutorial.MEDIUM:
        return u'medium'
    elif size == Tutorial.BIG:
        return u'big'
    else:
        raise NotImplementedError('No string for this size')


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


def export_part(part, export_all=True):
    """Export a part to a dict.

    Args:
        part: The part database model to export

    Returns:
        A dictionnary containing part data.

    """
    dct = OrderedDict()

    if export_all:
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
    dct['size'] = size_to_string(tutorial.size)
    dct['authors'] = [a.username for a in tutorial.authors.all()]
    dct['introduction'] = tutorial.introduction
    dct['conclusion'] = tutorial.conclusion

    if tutorial.size == Tutorial.SMALL:
        # We export the chapter without its empty title if small tutorial
        chapter = Chapter.objects.get(tutorial=tutorial)
        dct['chapter'] = export_chapter(chapter, export_all=False)

    elif tutorial.size == Tutorial.MEDIUM:
        # We export the part without its empty title if medium tutorial
        part = Part.objects.get(tutorial=tutorial)
        dct['part'] = export_part(part, export_all=False)

    elif tutorial.size == Tutorial.BIG:
        dct['parts'] = []
        parts = Part.objects\
            .filter(tutorial=tutorial)\
            .order_by('position_in_tutorial')
        for part in parts:
            dct['parts'].append(export_part(part))

    else:
        raise NotImplementedError('Export for this size does not exist')

    # If validation is requested and fails, just return empty dict
    if validate and not validate_tutorial(dct):
        return {}

    return dct


# Export-to-PDF functions using Pandoc

def export_title_md(f, title, level=1):
    """Write title into a file using markdown.

    Params:
        f: the file object to write in
        title: the title to write down
        level: level of the title, higher value means less important level

    """
    f.write(u'{} {}\n'.format(
        u''.join(repeat(u'#', level)),
        title,
    ))


def export_text_md(f, text):
    """Write text into a file using markdown.

    Params:
        f: the file object to write in
        text: the text to write down, unicode

    """
    if text:
        f.write(text)
        f.write(u'\n\n')


def export_extract_md(f, extract, level=1):
    """Write an extract into a file using markdown.

    Params:
        f: the file object to write in
        part: the extract to write down
        level: level of the extract title

    """
    export_title_md(f, extract.title, level)
    export_text_md(f, extract.text)


def export_chapter_md(f, chapter, level=1, export_all=True):
    """Write a chapter into a file using markdown.

    Params:
        f: the file object to write in
        part: the chapter to write down
        level: level of the chapter title, will be increased for sub items
        export_all: should the part metadata be written down?

    """
    if export_all:
        export_title_md(f, chapter.title, level)
        export_text_md(f, chapter.introduction)

    for extract in chapter.get_extracts():
        export_extract_md(f, extract, level + 1 if export_all else level)

    if export_all:
        export_text_md(f, chapter.conclusion)


def export_part_md(f, part, level=1, export_all=True):
    """Write a part into a file using markdown.

    Params:
        f: the file object to write in
        part: the part to write down
        level: level of the part title, will be increased for sub items
        export_all: should the part metadata be written down?

    """
    if export_all:
        export_title_md(f, part.title, level)
        export_text_md(f, part.introduction)

    for chapter in part.get_chapters():
        export_chapter_md(f, chapter, level + 1 if export_all else level)

    if export_all:
        export_text_md(f, part.conclusion)


def export_tutorial_pdf(tutorial):
    """Export a tutorial to a PDF file.

    This function uses Pandoc in order to generate the PDF file, using
    LaTeX intermediate source code. We simply generate a Markdown source file
    so that we do not have to convert the tutorial contents and then generate
    a PDF from this markdown file.

    Params:
        tutorial: the tutorial to render as PDF

    Returns:
        Path to the generated PDF file

    """

    # Generated document meta informations
    title = tutorial.title
    authors = u'; '.join([a.username for a in list(tutorial.authors.all())])
    date = datetime.now().strftime('%d/%m/%Y')

    base_dir = os.path.join(settings.MEDIA_ROOT, 'tutorials',
                            str(tutorial.pk))
    base_filepath = os.path.join(base_dir, tutorial.slug)

    # We try to create the directory if it does not exist
    try:
        os.mkdir(base_dir)
    except OSError:
        # Use FileExistsError for Python 3, not OSError
        pass

    # We will store both generated markdown and PDF into this directory
    md_filepath = u'{}.md'.format(base_filepath)
    pdf_filepath = u'{}.pdf'.format(base_filepath)

    # We write down the markdown source
    with io.open(md_filepath, 'w', encoding='utf-8') as f:
        f.write(u'% {}\n'.format(title))
        f.write(u'% {}\n'.format(authors))
        f.write(u'% {}\n'.format(date))

        f.write(u'\n\n')

        export_text_md(f, tutorial.introduction)

        if tutorial.size == Tutorial.BIG:
            for part in tutorial.get_parts():
                export_part_md(f, part)

        elif tutorial.size == Tutorial.MEDIUM:
            export_part_md(f, tutorial.get_parts()[0], export_all=False)

        elif tutorial.size == Tutorial.SMALL:
            export_chapter_md(f, tutorial.get_chapter(), export_all=False)

        export_text_md(f, tutorial.conclusion)

    # We generate the PDF from markdown using Pandoc
    pandoc_pdf.delay(md_filepath, pdf_filepath)

    return pdf_filepath
