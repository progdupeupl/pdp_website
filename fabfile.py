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

from os import path

from fabric.api import local, lcd

TEST_APPS = (
    'pdp.article',
    'pdp.tutorial',
    'pdp.forum',
    'pdp.member',
    'pdp.utils',
    'pdp.pages',
    'pdp.messages',
    'pdp.gallery')

ASSETS_DIR = path.join(path.dirname(__file__), 'assets/')


def syncdb():
    """Synchronise the Django database with the models."""
    local('python manage.py syncdb')


def migrate():
    """Run the south database migrations."""
    local('python manage.py migrate')


def makeassets():
    """Execute the Makefile in the ASSETS_DIR directory."""
    with lcd(ASSETS_DIR):
        local('make')


def collectstatic():
    """Collect and process all the static content."""
    local('python manage.py collectstatic --noinput')


def test():
    """Test all the project's own applications."""
    local('python manage.py test {0}'.format(' '.join(TEST_APPS)))


def coverage():
    """Launch coverage report."""
    local('coverage run --source="." manage.py test {0}'.format(
        ' '.join(TEST_APPS)))


def initsearch():
    """Initialise the search engine and its cache."""
    local('python manage.py rebuild_index --noinput')


def updatesearch():
    """Update the search engine cache."""
    local('python manage.py update_index')


def celery():
    """Start the celery tasks server."""
    local('celery worker --app=pdp.celeryapp:app')

def bootstrap():
    """Initialise the whole project for the first time."""
    syncdb()
    migrate()
    initsearch()
    makeassets()
    collectstatic()


try:
    from fabfile_local import *
except ImportError:
    pass
