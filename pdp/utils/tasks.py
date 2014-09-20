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

import os

from django.conf import settings
from celery import task


@task()
def pandoc_pdf(source, dest, tutorial_pk):
    """Generate PDF file from markdown source using Pandoc.

    Params:
        source: filepath to the markdown source file
        dest: name of the generated PDF file
        tutorial_pk: id of the tutorial

    """

    # Go to site’s root directory so the images can be found under '/media/'
    os.chdir(
        os.path.join(
            settings.MEDIA_ROOT,
            'tutorials/{}/'.format(tutorial_pk)
        )
    )

    # Generate PDF file using Pandoc
    pdf_dest = ''.join(dest.split('.')[:-1]) + '.pdf'
    command = '{}pandoc -s -t latex --latex-engine=xelatex -o {} {}'.format(
        settings.PANDOC_PATH,
        pdf_dest,
        source
    )
    os.system(command)
