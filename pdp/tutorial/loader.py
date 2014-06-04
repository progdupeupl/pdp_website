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
There is still some code refactoring to do but the module is working.

"""

import re
import io
from datetime import datetime

from pdp.tutorial.models import Tutorial, Part, Chapter, Extract


class NegativeTitleLevelError(Exception):
    pass


class InvalidLevelIncreaseError(Exception):
    pass


class EmptyTitleError(Exception):
    pass


class NoTitleFoundError(Exception):
    pass


class TutorialImporter(object):

    """Tool used to import tutorials into database models.

    You should only use this class by calling its load(fp) and run() methods
    unless you know what you do.
    """

    def __init__(self, author, size):
        self.author = author
        self.size = size

        self.tutorial = None
        self.lines = []
        self.titles = []

        # Level of the first title of the document
        self.initial_level = 0
        self.levels_to_match = []

        # Values of the previous title iteration
        self.last_matched_level = 0
        self.last_matched_num = 0

        # Static base items used for generation dependencies
        self.base_chapter = None
        self.base_part = None

        # Dynamic items used for generation
        self.extract = None
        self.chapter = None
        self.part = None

        # Position fields
        self.position_in_tutorial = 0
        self.position_in_part = 0
        self.position_in_chapter = 0

    def from_file(self, filepath):
        """Load a markdown source from a text file."""
        with io.open(filepath, 'r', encoding='utf-8') as f:
            self.lines = f.read().splitlines()

    def from_text(self, text):
        """Load a markdown source from an unicode string."""
        self.lines = text.splitlines()

    def deduce_level(self, sharps):
        """Deduce the level of a title based on its sharp amount."""
        return len(sharps)

    def deduce_initial_level(self):
        """Deduce initial level from first title."""
        if len(self.titles) > 0:
            self.initial_level = self.titles[0][1]
        else:
            self.initial_level = 0

    def deduce_levels_to_match(self):
        """Deduce the title levels to match during import."""
        levels_depth = 0

        # We generate a list of levels to match depending on the tutorial size
        # and create base_* elements depending on this size.
        if self.size == 'S':
            # Extract title
            levels_depth = 1
        elif self.size == 'M':
            # Chapter title + extract title
            levels_depth = 2
        elif self.size == 'B':
            # Part title + chapter title + extract title
            levels_depth = 3

        self.levels_to_match = list(map(
            lambda x: x + self.initial_level,
            range(1, levels_depth + 1)
        ))

    def extract_titles(self):
        """Match and extract all the titles out of the markdown document."""
        self.titles = []
        expr = re.compile("^(#+) (.+)$")

        for num, line in enumerate(self.lines):
            match = expr.match(line)
            if match:
                title = match.group(2)
                level = self.deduce_level(match.group(1))
                self.titles.append((num, level, title))

    def prepare_next_extract(self):
        """Save the previous extract in database and prepare a new one."""

        # Save previous extract (if any)
        if self.extract:
            self.extract.save()
            self.position_in_chapter += 1

        # Prepare new extract
        if self.size == 'S':
            chapter = self.base_chapter
        else:
            chapter = self.chapter

        self.extract = Extract(
            title=self.current_title,
            position_in_chapter=self.position_in_chapter,
            chapter=chapter
        )

    def prepare_next_chapter(self):
        """Save the previous chapter in database and prepare a new one."""

        # Save previous chapter (if any)
        if self.chapter:
            self.chapter.save()
            self.position_in_chapter = 0
            self.position_in_part += 1

        # Prepare new chapter
        if self.size == 'M':
            part = self.base_part
        else:
            part = self.part

        self.chapter = Chapter(
            title=self.current_title,
            position_in_part=self.position_in_part,
            part=part
        )

    def prepare_next_part(self):
        """Save the previous part in database and prepare a new one."""

        # Save previous part (if any)
        if self.part:
            self.part.save()
            self.position_in_chapter = 0
            self.position_in_part = 0
            self.position_in_tutorial += 1

        # Prepare new part
        self.part = Part(
            title=self.current_title,
            position_in_tutorial=self.position_in_tutorial,
            tutorial=self.tutorial
        )

    def check_titles(self):
        """Check that the source is correctly formatted.

        This will run some assert() calls all over the loaded structure of
        titles. You can catch AssertError in order to know that the user input
        is wrong, until more precise exceptions.
        """

        if len(self.titles) == 0:
            raise NoTitleFoundError

        # We cannot perform tests on titles if there is only one
        if len(self.titles) == 1:
            return

        previous_level = self.initial_level

        # We loop on all titles except the first one
        for num, level, title in self.titles[1:]:
            # The line has to be bounded inside self.lines
            assert(num >= 0 and num < len(self.lines))

            # All titles must have a superior level than the main title
            if level <= self.initial_level:
                raise NegativeTitleLevelError

            if len(title) <= 0:
                raise EmptyTitleError

            # If ascending level we must be sure that it is increasing by
            # maximum 1 or staying at 0.
            if level > previous_level:
                if level - previous_level > 1:
                    raise InvalidLevelIncreaseError

            previous_level = level

    def prepare_base_items(self):
        """Create the base database items and save them for the import.

        This will save optional Part and Chapter depending on the size of the
        tutorial, plus the Tutorial database instance itself.
        """
        # We create the initial tutorial database element
        self.tutorial = Tutorial(
            title=self.titles[0][2],
            size=self.size,
            pubdate=datetime.now()
        )

        # We save it for the first time in order to make the m2m relations work
        self.tutorial.save()

        self.tutorial.authors.add(self.author)

        # Create required base elements depending on tutorial size
        if self.size == 'S':
            self.base_chapter = Chapter(tutorial=self.tutorial)
            self.base_chapter.save()

        elif self.size == 'M':
            self.base_part = Part(tutorial=self.tutorial)
            self.base_part.save()

    def finish_text_import(self):
        """Finish the import process once every title has been parsed."""
        content = "\n".join(self.lines[self.last_matched_num + 1:])

        if self.base_chapter:

            if self.last_matched_level == self.levels_to_match[0]:
                self.extract.text = content
                self.extract.save()
            else:
                self.tutorial.introduction = content
                self.tutorial.save()

        elif self.base_part:
            if self.current_level == self.levels_to_match[0]:

                if self.last_matched_level == self.levels_to_match[0]:
                    self.chapter.introduction = content
                    self.chapter.save()
                elif self.last_matched_level == self.levels_to_match[1]:
                    self.extract.text = content
                    self.extract.save()

            else:

                if self.last_matched_level == self.levels_to_match[0]:
                    self.chapter.introduction = content
                    self.chapter.save()
                elif self.last_matched_level == self.levels_to_match[1]:
                    self.extract.text = content
                    self.extract.save()

        else:
            if self.current_level == self.levels_to_match[0]:

                if self.last_matched_level == self.levels_to_match[0]:
                    self.part.introduction = content
                    self.part.save()
                elif self.last_matched_level == self.levels_to_match[1]:
                    self.chapter.introduction = content
                    self.chapter.save()
                elif self.last_matched_level == self.levels_to_match[2]:
                    self.extract.text = content
                    self.extract.save()

            elif self.current_level == self.levels_to_match[1]:

                # Update content
                if self.last_matched_level == self.levels_to_match[0]:
                    self.part.introduction = content
                    self.part.save()
                elif self.last_matched_level == self.levels_to_match[1]:
                    self.chapter.introduction = content
                    self.chapter.save()
                elif self.last_matched_level == self.levels_to_match[2]:
                    self.extract.text = content
                    self.extract.save()

            else:

                # Update content
                if self.last_matched_level == self.levels_to_match[0]:
                    self.part.introduction = content
                    self.part.save()
                elif self.last_matched_level == self.levels_to_match[1]:
                    self.chapter.introduction = content
                    self.chapter.save()
                elif self.last_matched_level == self.levels_to_match[2]:
                    self.extract.text = content
                    self.extract.save()

    def to_database(self):
        """Loop over the titles in order to convert them to database instances.

        This will create the corresponding Part, Chapter and Extract elements
        based on the input and fill their introduction/text fields with rest
        of the markdown.
        """
        # We remember the last level we matched in order to recognize
        # introductions for elements.
        self.last_matched_level = self.initial_level
        self.last_matched_num = self.titles[0][1]

        for self.current_num, self.current_level, self.current_title in \
                self.titles[1:]:

            # If the level is in the list, we have to create a database element
            # out of if. Elsewise this title is considered as Markdown title.
            if self.current_level in self.levels_to_match:

                # If we were matching markdown before, we stop the match
                # process since we are changing level and add markdown content
                # to the revelant place.
                #
                # We start at (last_matched_num + 1) in order to not catch last
                # processed title in the content.
                content = "\n".join(
                    self.lines[self.last_matched_num + 1:self.current_num]
                )

                # If we were under the first title, we update tutorial's
                # introduction.
                if self.last_matched_level == self.initial_level:
                    self.tutorial.introduction = content
                    self.tutorial.save()

                # Small tutorial, obviously it is an extract
                if self.base_chapter:

                    # Update content
                    if self.last_matched_level == self.levels_to_match[0]:
                        self.extract.text = content

                    self.prepare_next_extract()

                # Medium tutorial, it is a chapter or an extract
                elif self.base_part:
                    if self.current_level == self.levels_to_match[0]:

                        # Update content
                        if self.last_matched_level == self.levels_to_match[0]:
                            self.chapter.introduction = content
                        elif self.last_matched_level == \
                                self.levels_to_match[1]:
                            self.extract.text = content
                            self.extract.save()

                        self.prepare_next_chapter()

                    else:

                        # Update content
                        if self.last_matched_level == self.levels_to_match[0]:
                            self.chapter.introduction = content
                            self.chapter.save()
                        elif self.last_matched_level == \
                                self.levels_to_match[1]:
                            self.extract.text = content

                        self.prepare_next_extract()

                # Big tutorial, it is a part or a chapter or an extract
                else:
                    if self.current_level == self.levels_to_match[0]:

                        # Update content
                        if self.last_matched_level == \
                                self.levels_to_match[0]:
                            self.part.introduction = content
                        elif self.last_matched_level == \
                                self.levels_to_match[1]:
                            self.chapter.introduction = content
                            self.chapter.save()
                        elif self.last_matched_level == \
                                self.levels_to_match[2]:
                            self.extract.text = content
                            self.extract.save()

                        self.prepare_next_part()

                    elif self.current_level == self.levels_to_match[1]:

                        # Update content
                        if self.last_matched_level == \
                                self.levels_to_match[0]:
                            self.part.introduction = content
                            self.part.save()
                        elif self.last_matched_level == \
                                self.levels_to_match[1]:
                            self.chapter.introduction = content
                        elif self.last_matched_level == \
                                self.levels_to_match[2]:
                            self.extract.text = content
                            self.extract.save()

                        self.prepare_next_chapter()

                    else:

                        # Update content
                        if self.last_matched_level == \
                                self.levels_to_match[0]:
                            self.part.introduction = content
                            self.part.save()
                        elif self.last_matched_level == \
                                self.levels_to_match[1]:
                            self.chapter.introduction = content
                            self.chapter.save()
                        elif self.last_matched_level == \
                                self.levels_to_match[2]:
                            self.extract.text = content

                        self.prepare_next_extract()

                self.last_matched_level = self.current_level
                self.last_matched_num = self.current_num

        # At this point we have matched all titles. we finally need to finish
        # markdown import for the last matched title till end of file.
        self.finish_text_import()

    def run(self):
        """Start the import process."""
        self.extract_titles()
        self.deduce_initial_level()
        self.check_titles()
        self.prepare_base_items()
        self.deduce_levels_to_match()
        self.to_database()
