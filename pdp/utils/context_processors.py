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

"""Module containing some custom context processors."""

from django.conf import settings


def git_version(request):
    """Return the current deployed git version.

    If not running on a production machine (if the 'git_version.txt' file is
    not found), this will just display that the running version is local.

    """

    local = False
    v = ''
    try:
        with open('git_version.txt') as f:
            v = f.read()
    except IOError:
        local = True

    if local:
        return {
            'git_version': 'local_version',
            'git_hash': None,
        }

    return {
        'git_version': v,
        'git_hash': v[-8:],
    }


def analytics_key(request):
    """Return Google Analytics key, if set.

    Returns:
        string or None

    """
    try:
        key = settings.ANALYTICS_KEY
    except ImportError:
        key = None

    return {
        'analytics_key': key
    }
