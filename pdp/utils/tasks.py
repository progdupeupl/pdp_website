# coding: utf-8

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
