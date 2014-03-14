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

"""Module containing some custom context processors."""

import sys

import django


def versions(request):
    """Return the current version of Python and Django."""
    return {
        'django_version': '{0}.{1}.{2}'.format(
            django.VERSION[0], django.VERSION[1], django.VERSION[2]),
        'python_version': '{0}.{1}.{2}'.format(
            sys.version_info[0], sys.version_info[1], sys.version_info[2])
    }


def git_version(request):
    """Return the current deployed git version.

    If not running on a production machine (if the 'git_version.txt' file is
    not found), this will just display that the running version is local.

    """
    try:
        with open('git_version.txt') as f:
            v = f.read()
    except IOError:
        v = 'local_version'

    return {
        'git_version': v
    }
