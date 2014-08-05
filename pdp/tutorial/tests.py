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

from django.test import TestCase

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from django_dynamic_fixture import G

from pdp.tutorial.models import Tutorial, Part, Chapter, get_last_tutorials
from pdp.member.models import Profile


class GetLastTutorialsTests(TestCase):
    """Tests for the get_last_tutorials function."""

    def test_last_tutorials_zero(self):
        """Tests if the get_last_tutorials work with no visible tutorial."""
        self.assertEqual(0, len(get_last_tutorials()))
        G(Tutorial, is_visible=False)
        self.assertEqual(0, len(get_last_tutorials()))

    def test_last_tutorials_one(self):
        """Tests that get_last_tutorials work if there is only one."""
        tutorial = G(Tutorial, is_visible=True)
        self.assertEqual(1, len(get_last_tutorials()))
        self.assertEqual(tutorial, get_last_tutorials()[0])

    def test_last_tutorials_many(self):
        """Tests that the last tutorials works correctly."""
        tutorials = []
        for n in range(2000, 1900, -1):
            tutorial = G(Tutorial)
            tutorials.append(tutorial)

        last = get_last_tutorials()

        for n, val in enumerate(last):
            self.assertEqual(val, tutorials[n])


class TutorialIntegrationTests(TestCase):
    def test_url_index(self):
        """Tests viewing the index page of tutorials."""
        resp = self.client.get('/tutoriels/')
        self.assertEqual(200, resp.status_code)

    def test_url_new_tutorial(self):
        """Tests adding a new tutorial as anonymous."""
        resp = self.client.get('/tutoriels/nouveau/tutoriel')
        self.assertEqual(302, resp.status_code)

    def test_url_view_tutorial_invisible(self):
        """Testing viewing an invisible tutorial as anonymous."""
        tutorial = G(Tutorial, is_visible=False)
        resp = self.client.get(tutorial.get_absolute_url())
        self.assertEqual(404, resp.status_code)

    def test_url_view_tutorial_visible(self):
        """Testing viewing a visible tutorial as anonymous."""
        tutorial = G(Tutorial, is_visible=True, size=Tutorial.BIG)
        resp = self.client.get(tutorial.get_absolute_url())
        self.assertEqual(200, resp.status_code)

    def test_url_view_part_invisible(self):
        """Testing viewing a part from invisible tutorial as anonymous."""
        tutorial = G(Tutorial, is_visible=False, size=Tutorial.BIG)
        part = G(Part, tutorial=tutorial)
        resp = self.client.get(part.get_absolute_url())
        self.assertEqual(403, resp.status_code)

    def test_url_view_part_visible(self):
        """Testing viewing a part from visible tutorial as anonymous."""
        tutorial = G(Tutorial, is_visible=True, size=Tutorial.BIG)
        part = G(Part, tutorial=tutorial)
        resp = self.client.get(part.get_absolute_url())
        self.assertEqual(200, resp.status_code)

    # Commands as unlogged user

    def test_url_create_tutorial_anon(self):
        """Testing creating a tutorial as anonymous."""
        resp = self.client.get(reverse('pdp.tutorial.views.add_tutorial'))
        self.assertEqual(302, resp.status_code)

    def test_url_import_tutorial_anon(self):
        """Testing importing a tutorial as anonymous."""
        resp = self.client.get(reverse('pdp.tutorial.views.import_tutorial'))
        self.assertEqual(302, resp.status_code)

    def test_url_create_part_anon(self):
        """Testing creating a part as anonymous."""
        G(Tutorial, is_visible=True)
        resp = self.client.get(reverse('pdp.tutorial.views.add_part'))
        self.assertEqual(302, resp.status_code)

    def test_url_create_chapter_anon(self):
        """Testing creating a chapter as anonymous."""
        tutorial = G(Tutorial, is_visible=True, size=Tutorial.BIG)
        part = G(Part, tutorial=tutorial)
        resp = self.client.get(u''.join(
            (reverse('pdp.tutorial.views.add_chapter'),
             '?partie={}'.format(part.pk))))
        self.assertEqual(302, resp.status_code)


class BigTutorialIntegrationTests(TestCase):
    def setUp(self):
        self.tutorial = G(
            Tutorial,
            pk=42,
            title=u'Test tutorial',
            is_visible=True,
            size=Tutorial.BIG,
        )

        self.parts = [G(
            Part,
            pk=21,
            title=u'Test part',
            tutorial=self.tutorial
        )]

    def test_url_download(self):
        """Test downloading a big tutorial.

        Since we need Pandoc and Gunicorn for PDF export, we are only testing
        JSON export here.

        """
        resp = self.client.get(u''.join(
            (reverse('pdp.tutorial.views.download'),
             '?tutoriel={}&format=json'.format(self.tutorial.pk))))
        self.assertEqual(200, resp.status_code)


class MediumTutorialIntegrationTests(TestCase):
    def setUp(self):
        self.author = G(User, username='test')
        self.tutorial = G(
            Tutorial,
            title=u'Test tutorial',
            is_visible=True,
            authors=[self.author],
            size=Tutorial.MEDIUM,
        )

        self.part = G(
            Part,
            tutorial=self.tutorial
        )

    def test_url_download(self):
        """Test downloading a medium tutorial.

        Since we need Pandoc and Gunicorn for PDF export, we are only testing
        JSON export here.

        """
        resp = self.client.get(u''.join(
            (reverse('pdp.tutorial.views.download'),
             '?tutoriel={}&format=json'.format(self.tutorial.pk))))
        self.assertEqual(200, resp.status_code)


class SmallTutorialIntegrationTests(TestCase):
    def setUp(self):
        self.tutorial = G(
            Tutorial,
            title=u'Test tutorial',
            is_visible=True,
            size=Tutorial.SMALL,
        )

        G(Chapter, tutorial=self.tutorial)

    # Does not work, have no idea why
    # def test_url_download(self):find_tutorial
    #    resp = self.client.get(u''.join(
    #        (reverse('pdp.tutorial.views.download'),
    #         '?tutoriel={}'.format(self.tutorial.pk))))
    #    self.assertEqual(200, resp.status_code)


class TutorialSearchIntegrationTests(TestCase):
    def setUp(self):
        self.user = G(User, username='test')
        self.profile = G(Profile, user=self.user)

    def test_url_by_author_none(self):
        resp = self.client.get(
            reverse('pdp.tutorial.views.by_author',
                    args=[self.user.username]))

        self.assertEqual(resp.status_code, 200)

    def test_url_by_author_invisible(self):
        G(
            Tutorial,
            is_visible=False,
            author=self.user
        )

        resp = self.client.get(
            reverse('pdp.tutorial.views.by_author',
                    args=[self.user.username]))

        self.assertEqual(resp.status_code, 200)

    def test_url_by_author_visible(self):
        G(
            Tutorial,
            is_visible=True,
            author=self.user,
        )

        resp = self.client.get(
            reverse('pdp.tutorial.views.by_author',
                    args=[self.user.username]))

        self.assertEqual(resp.status_code, 200)

    def test_url_by_category_all(self):
        resp = self.client.get(
            reverse('pdp.tutorial.views.by_category', args=['tous'])
        )
        self.assertEqual(resp.status_code, 200)

    def test_url_by_category_beta(self):
        """Test viewing beta tutorials as an unlogged used."""
        resp = self.client.get(
            reverse('pdp.tutorial.views.by_category', args=['beta'])
        )
        self.assertEqual(resp.status_code, 403)

    def test_url_by_category_other(self):
        resp = self.client.get(
            reverse('pdp.tutorial.views.by_category', args=['autres'])
        )
        self.assertEqual(resp.status_code, 200)


class AuthenticatedSearchIntegrationTests(TestCase):
    def setUp(self):
        # Create user
        self.user = G(User, username='test')
        self.user.set_password('test')
        self.user.save()

        # Create profile
        self.profile = G(Profile, user=self.user)

        # Authenticate user
        self.client.login(username='test', password='test')

    def test_url_by_category_beta(self):
        """Test viewing beta tutorials as a logged used."""
        resp = self.client.get(
            reverse('pdp.tutorial.views.by_category', args=['beta'])
        )
        self.assertEqual(resp.status_code, 200)


class AuthenticatedTutorialIntegrationTests(TestCase):
    def setUp(self):
        # Create user
        self.user = G(User, username='test')
        self.user.set_password('test')
        self.user.save()

        # Create profile
        self.profile = G(Profile, user=self.user)

        # Authenticate user
        self.client.login(username='test', password='test')

    def test_url_add_tutorial(self):
        resp = self.client.get(reverse('pdp.tutorial.views.add_tutorial'))
        self.assertEqual(resp.status_code, 200)

    def test_url_import_tutorial(self):
        resp = self.client.get(reverse('pdp.tutorial.views.import_tutorial'))
        self.assertEqual(resp.status_code, 200)


class FeedsIntegrationTests(TestCase):

    def test_tutorials_feed_rss(self):
        resp = self.client.get('/tutoriels/flux/rss/')
        self.assertEqual(resp.status_code, 200)

    def test_tutorials_feed_atom(self):
        resp = self.client.get('/tutoriels/flux/atom/')
        self.assertEqual(resp.status_code, 200)
