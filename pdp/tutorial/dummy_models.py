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

"""Fake models for tutorial app.

These fake models are used to simulate algorithms with database interactions.
On each call to save() on a given model, the model will not be saved at all but
a log line will be printed with model status at save call.

This is used to test database interaction algorithms like import in the
prototyping stage in order to see if the calls are done in the right amount, at
the good time.
"""

class Tutorial:
    def __init__(self, title="", size="", authors=[]):
        self.title = title
        self.introduction = ""
        self.size = size
        self.authors = authors

    def __repr__(self):
        return "<Tutorial title={} authors={}>".format(
            self.title,
            self.authors
        )

    def save(self):
        print("SAVE {}".format(self.__repr__()))
        print(self.introduction.__repr__())


class Part:
    def __init__(self, title="", tutorial=None, position_in_tutorial=-1):
        self.tutorial = tutorial
        self.title = title
        self.introduction = ""
        self.position_in_tutorial = position_in_tutorial

    def __repr__(self):
        return "<Part title={} position={} tutorial={}>".format(
            self.title,
            self.position_in_tutorial,
            self.tutorial
        )

    def save(self):
        print("SAVE {}".format(self.__repr__()))
        print(self.introduction.__repr__())


class Chapter:
    def __init__(self, tutorial=None, part=None, title="", position_in_part=-1):
        self.tutorial = tutorial
        self.part = part
        self.title = title
        self.introduction = ""
        self.position_in_part = position_in_part

    def __repr__(self):
        return "<Chapter title={} position={} tutorial={} part={}>".format(
            self.title,
            self.position_in_part,
            self.tutorial,
            self.part
        )

    def save(self):
        print("SAVE {}".format(self.__repr__()))
        print(self.introduction.__repr__())


class Extract:
    def __init__(self, chapter=None, title="", position_in_chapter=-1):
        self.chapter = chapter
        self.title = title
        self.text = ""
        self.position_in_chapter = position_in_chapter

    def __repr__(self):
        return "<Extract title={} position={} chapter={}>".format(
            self.title,
            self.position_in_chapter,
            self.chapter
        )

    def save(self):
        print("SAVE {}".format(self.__repr__()))
        print(self.text.__repr__())
