from fabric.api import local

TEST_APPS = ('article', 'tutorial', 'forum', 'member', 'utils', 'pages')


def test():
    local('python manage.py test %s' % ' '.join(TEST_APPS))


try:
    from fabfile_local import *
except ImportError:
    pass
