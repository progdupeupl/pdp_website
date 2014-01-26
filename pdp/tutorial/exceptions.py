# coding: utf-8

"""Exceptions for tutorial app."""

class CorruptedTutorialError(Exception):
    """Exception thrown when a tutorial is corrupted."""
    def __init__(self, reason):
        self.reason = reason

    def __str__(self):
        return repr(self.reason)


class OrphanPartException(Exception):
    """Exception thrown when a part is orphan."""
    pass

class OrphanChapterException(Exception):
    """Exception thrown when a chapter is orphan."""
    pass
