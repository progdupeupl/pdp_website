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

"""File containing celery tasks for long tasks."""

import subprocess

from celery import task


@task()
def pandoc_pdf(source, dest):
    """Generate PDF file from markdown source using Pandoc.

    Params:
        source: filepath to the markdown source file
        dest: name of the generated PDF file

    """
    subprocess.call(['pandoc', '--latex-engine=xelatex', '-o', dest, source])
