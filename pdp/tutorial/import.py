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

"""Import functions for tutorials.

This module allow import of tutorial from Markdown source to database models.
Since this is still WIP, we are using dummy models and a main here to test that
import is fine on different sizes of tutorials, and in order to test it over
some markdown sources
"""

import sys
import re

from pdp.tutorial.dummy_models import Tutorial, Part, Chapter, Extract


class TutorialImporter(object):
    def __init__(self):
        self.lines = []
        self.titles = []
        self.initial_level = 0

    def load(self, filepath):
        with open(filepath, "r") as f:
            self.lines = f.read().splitlines()

    def deduce_level(self, sharps):
        return len(sharps)

    def extract_titles(self):
        self.titles = []
        expr = re.compile("^(#+) (.+)$")

        for num, line in enumerate(self.lines):
            match = expr.match(line)
            if match:
                title = match.group(2)
                level = self.deduce_level(match.group(1))
                self.titles.append((num, level, title))

        # Deduce initial level from first title
        if len(self.titles) > 0:
            self.initial_level = self.titles[0][1]
        else:
            self.initial_level = 0

    def check_titles(self):
        # We cannot perform tests on titles if there is only one
        assert(len(self.titles) > 1)

        previous_level = self.initial_level

        # We loop on all titles except the first one
        for num, level, title in self.titles[1:]:
            # The line has to be bounded inside self.lines
            assert(num >= 0 and num < len(self.lines))

            # All titles must have a superior level than the main title
            assert(level > self.initial_level)
            assert(len(title) > 0)

            # If ascending level we must be sure that it is increasing by
            # maximum 1 or staying at 0.
            if level > previous_level:
                assert(level - previous_level <= 1)

            previous_level = level

    def to_database(self, size):
        # We create the initial tutorial database element
        tutorial = Tutorial(
            title=self.titles[0][2],
            size=size
        )

        # We save it for the first time in order to make the m2m relations work
        tutorial.save()

        # Deduce depth of levels to match for database elements
        levels_depth = 0

        # Static base items used for generation dependencies
        base_chapter = None
        base_part = None

        # Dynamic items used for generation
        extract = None
        chapter = None
        part = None

        # We generate a list of levels to match depending on the tutorial size
        # and create base_* elements depending on this size.
        if size == 'S':
            # Extract title
            levels_depth = 1
            base_chapter = Chapter(tutorial=tutorial)
            base_chapter.save()
        elif size == 'M':
            # Chapter title + extract title
            levels_depth = 2
            base_part = Part(tutorial=tutorial)
            base_part.save()
        elif size == 'B':
            # Part title + chapter title + extract title
            levels_depth = 3

        levels_to_match = list(map(
            lambda x: x + self.initial_level,
            range(1, levels_depth + 1)
        ))

        # We remember the last level we matched in order to recognize
        # introductions for elements.
        last_matched_level = self.initial_level
        last_matched_num = 0

        for num, level, title in self.titles[1:]:

            # If the level is in the list, we have to create a database element
            # out of if. Elsewise this title is considered as Markdown title.
            if level in levels_to_match:

                # If we were matching markdown before, we stop the match
                # process since we are changing level and add markdown content
                # to the revelant place.
                content = "\n".join(self.lines[last_matched_num:num])

                # If we were under the first title, we update tutorial's
                # introduction.
                if last_matched_level == self.initial_level:
                    tutorial.introduction = content
                    tutorial.save()

                # Small tutorial, obviously it is an extract
                if base_chapter:

                    # Update content
                    if last_matched_level == levels_to_match[0]:
                        extract.text = content

                    # Save previous extract
                    if extract:
                        extract.save()

                    # Prepare new extract
                    extract = Extract(
                        title=title,
                        chapter=base_chapter
                    )

                # Medium tutorial, it is a chapter or an extract
                elif base_part:
                    if level == levels_to_match[0]:

                        # Update content
                        if last_matched_level == levels_to_match[0]:
                            chapter.introduction = content
                        elif last_matched_level == levels_to_match[1]:
                            extract.text = content

                        # Save previous chapter
                        chapter.save()

                        # Prepare new chapter
                        chapter = Chapter(
                            title=title,
                            part=base_part
                        )

                    else:

                        # Update content
                        if last_matched_level == levels_to_match[0]:
                            chapter.introduction = content
                        elif last_matched_level == levels_to_match[1]:
                            extract.text = content

                        # Save previous extract
                        extract.save()

                        # Prepare new extract
                        extract = Extract(
                            title=title,
                            chapter=chapter
                        )

                # Big tutorial, it is a part or a chapter or an extract
                else:
                    if level == levels_to_match[0]:

                        # Update content
                        if last_matched_level == levels_to_match[0]:
                            part.introduction = content
                        elif last_matched_level == levels_to_match[1]:
                            chapter.introduction = content
                        elif last_matched_level == levels_to_match[2]:
                            extract.text = content

                        # Save previous part
                        part.save()

                        # Prepare new part
                        part = Part(
                            title=title,
                            tutorial=tutorial
                        )

                    elif level == levels_to_match[1]:

                        # Update content
                        if last_matched_level == levels_to_match[0]:
                            part.introduction = content
                        elif last_matched_level == levels_to_match[1]:
                            chapter.introduction = content
                        elif last_matched_level == levels_to_match[2]:
                            extract.text = content

                        # Save previous chapter
                        chapter.save()

                        # Prepare new chapter
                        chapter = Chapter(
                            title=title,
                            part=part
                        )

                    else:

                        # Update content
                        if last_matched_level == levels_to_match[0]:
                            part.introduction = content
                        elif last_matched_level == levels_to_match[1]:
                            chapter.introduction = content
                        elif last_matched_level == levels_to_match[2]:
                            extract.text = content

                        # Save previous extract
                        extract.save()

                        # Prepare new extract
                        extract = Extract(
                            title=title,
                            chapter=chapter
                        )

                last_matched_level = level
                last_matched_num = num


if __name__ == "__main__":

    # usage: python import.py my_tutorial.md

    ti = TutorialImporter()

    ti.load(sys.argv[1])

    ti.extract_titles()
    ti.check_titles()

    # Check that the titles are correct after check
    print(ti.titles)

    # Yeah let's simulate this with dummy models
    ti.to_database('S')
