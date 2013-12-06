# coding: utf-8

"""Module used to display beautiful folded paginators."""


def paginator_range(current, stop, start=1):
    """Generate a folded paginator range.

    Args:
        current: current page of the paginator
        stop: last page of the paginator
        start: first page of the paginator

    Returns:
        A list containing integers (page numbers to be displayed) and sometimes
        some None too (folding point to be displayed as three dots for
        example).

    Raises:
        ValueError

    """

    if current > stop:
        raise ValueError("Current value should not be greater than maximum")

    # Basic case when no folding
    if stop - start <= 4:
        return range(start, stop + 1)

    # Complex case when folding
    lst = []
    for i in range(start, stop + 1):
        # Bounds
        if i == start or i == stop:
            lst.append(i)
            if i == start and not current - start <= 2:
                lst.append(None)
        # Neighbors
        elif 0 < abs(i - current) <= 1:
            lst.append(i)
            if i - current > 0 and not stop - i <= 2:
                lst.append(None)
        # Current
        elif i == current:
            lst.append(i)
        # LOL
        elif i == stop - 1 and current == stop - 3:
            lst.append(i)
        # And ignore all other numbers

    return lst
