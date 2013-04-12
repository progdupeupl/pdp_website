# coding: utf-8


def move(obj, new_pos, position_f, parent_f, children_fn):
    '''
    Move an object and reorder other objects affected by moving.

    This function need the object, the new position you want the object to go,
    the position field name of the object (eg. 'position_in_chapter'), the
    parent field of the object (eg. 'chapter') and the children function's
    name to apply to parent (eg. 'get_extracts').

    Example for extracts :

      move(extract, new_pos, 'position_in_chapter', 'chapter', 'get_extracts')

    '''
    old_pos = getattr(obj, position_f)
    objects = getattr(getattr(obj, parent_f), children_fn)()

    # Check that asked new position is correct
    if not 1 <= new_pos <= objects.count():
        raise ValueError('Can\'t move object to position %s' % new_pos)

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
    obj.save()
