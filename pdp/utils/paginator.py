# coding: utf-8


def paginator_range(current, stop, start=1):
    assert(current <= stop)

    lst = []
    for i in range(start, stop + 1):
        # Bounds
        if i == start or i == stop:
            lst.append(i)
            if i == start and not current - start < 2:
                lst.append(None)
        # Neighbors
        elif 0 < abs(i - current) <= 1:
            lst.append(i)
            if i - current > 0 and not stop - i < 2:
                lst.append(None)
        # Current
        elif i == current:
            lst.append(i)
        # And ignore all other numbers

    return lst
