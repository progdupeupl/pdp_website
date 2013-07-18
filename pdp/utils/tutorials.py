# coding: utf-8

from collections import OrderedDict

from pdp.tutorial.models import Part, Chapter, Extract


def move(obj, new_pos, position_f, parent_f, children_fn):
    '''
    Move an object and reorder other objects affected by moving.

    This function need the object, the new position you want the object to go,
    the position field name of the object (eg. 'position_in_chapter'), the
    parent field of the object (eg. 'chapter') and the children function's
    name to apply to parent (eg. 'get_extracts').

    You will still have to save the object once modified.

    Example for extracts :

      move(extract, new_pos, 'position_in_chapter', 'chapter', 'get_extracts')

    '''
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
    '''
    Export a chapter to a dict
    '''
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
    '''
    Export a part to a dict
    '''
    dct = OrderedDict()
    dct['title'] = part.title
    dct['chapters'] = []

    chapters = Chapter.objects\
        .filter(part=part)\
        .order_by('position_in_part')
    for chapter in chapters:
        dct['chapters'].append(export_chapter(chapter))

    return dct


def export_tutorial(tutorial):
    '''
    Export a tutorial to a dict
    '''
    dct = OrderedDict()
    dct['title'] = tutorial.title
    dct['description'] = tutorial.description
    dct['is_mini'] = tutorial.is_mini
    dct['authors'] = [a.username for a in tutorial.authors.all()]
    dct['introduction'] = tutorial.introduction
    dct['conclusion'] = tutorial.conclusion

    if tutorial.is_mini:
        # We export the chapter without its empty title if mini tutorial
        chapter = Chapter.objects.get(tutorial=tutorial)
        dct['chapter'] = export_chapter(chapter, export_all=False)
    else:
        dct['parts'] = []
        parts = Part.objects\
            .filter(tutorial=tutorial)\
            .order_by('position_in_tutorial')
        for part in parts:
            dct['parts'].append(export_part(part))

    return dct
