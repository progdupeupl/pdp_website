from fabric.api import local

TEST_APPS = ('article', 'tutorial', 'forum', 'member', 'utils', 'pages')


def test():
    local('python manage.py test {0}'.format(' '.join(TEST_APPS)))


try:
    from fabfile_local import *
except ImportError:
    pass
