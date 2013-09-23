from os import path

from fabric.api import local, lcd

TEST_APPS = ('article', 'tutorial', 'forum', 'member', 'utils', 'pages')
ASSETS_DIR = path.join(path.dirname(__file__), 'assets/')


def syncdb():
    local('python manage.py syncdb')


def migrate():
    local('python manage.py migrate')


def makeassets():
    with lcd(ASSETS_DIR):
        local('make')


def collectstatic():
    local('python manage.py collectstatic --no-input')


def test():
    local('python manage.py test {0}'.format(' '.join(TEST_APPS)))


def initsearch():
    local('python manage.py rebuild_index --noinput')


def updatesearch():
    local('python manage.py update_index')


def bootstrap():
    syncdb()
    migrate()
    initsearch()
    makeassets()
    collectstatic()


try:
    from fabfile_local import *
except ImportError:
    pass
