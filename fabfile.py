from os import path

from fabric.api import local, lcd

TEST_APPS = (
    'pdp.article',
    'pdp.tutorial',
    'pdp.forum',
    'pdp.member',
    'pdp.utils',
    'pdp.pages',
    'pdp.messages')

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


def initsearch():
    """Initialise the search engine and its cache."""
    local('python manage.py rebuild_index --noinput')


def updatesearch():
    """Update the search engine cache."""
    local('python manage.py update_index')


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
