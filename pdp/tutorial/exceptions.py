# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

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
