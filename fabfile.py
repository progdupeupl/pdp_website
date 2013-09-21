from fabric.api import local

TEST_APPS = ('article', 'tutorial', 'forum', 'member', 'utils', 'pages')


def test():
    local('python manage.py test {0}'.format(' '.join(TEST_APPS)))


def initsearch():
    local('python manage.py rebuild_index')


def updatesearch():
    local('python manage.py update_index')

try:
    from fabfile_local import *
except ImportError:
    pass
