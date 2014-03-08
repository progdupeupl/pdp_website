# coding: utf-8

"""A small module for handling some common operations on articles."""

from collections import OrderedDict

import os
import io
from datetime import datetime

from pdp.utils.schemas import validate_article

from pdp import settings

from pdp.utils.tasks import pandoc_pdf

# Export-to-dict functions


def export_article(article, validate=True):
    """Export an article to a dict.

    Args:
        article: The article database model to export
        validate: Should the output dictionnary be checked?

    Returns:
        A dictionnary containing article data. If validate option is set and
        the validation fails, it will fail silently returning an empty
        dictionnary instead.

    """

    dct = OrderedDict()
    dct['title'] = article.title
    dct['description'] = article.description
    dct['author'] = article.author.username
    dct['tags'] = [tag.__unicode__() for tag in article.tags.all()]
    dct['text'] = article.text

    if validate and not validate_article(dct):
        return {}

    return dct


# Export-to-PDF functions using Pandoc

def export_article_pdf(article):
    """Export an article to a PDF file.

    This function uses Pandoc in order to generate the PDF file, using
    LaTeX intermediate source code. We simply generate a Markdown source file
    so that we do not have to convert the article contents and then generate
    a PDF from this markdown file.

    Params:
        article: the article to render as PDF

    Returns:
        Path to the generated PDF file

    """

    # Generated document meta informations
    title = article.title
    author = article.author
    date = datetime.now().strftime('%d/%m/%Y')

    base_dir = os.path.join(settings.MEDIA_ROOT, 'articles', str(article.pk))
    base_filepath = os.path.join(base_dir, article.slug)

    # We try to create the directory if it does not exist
    try:
        os.mkdir(base_dir)
    except OSError:
        # Use FileExistsError for Python 3, not OSError
        pass

    # We will store both generated markdown and PDF into this directory
    md_filepath = u'{}.md'.format(base_filepath)
    pdf_filepath = u'{}.pdf'.format(base_filepath)

    # We write down the markdown source
    with io.open(md_filepath, 'w', encoding='utf-8') as f:
        f.write(u'% {}\n'.format(title))
        f.write(u'% {}\n'.format(author))
        f.write(u'% {}\n'.format(date))

        f.write(u'\n\n')

        if article.text:
            f.write(article.text)

    # We generate the PDF from markdown using Pandoc
    pandoc_pdf.delay(md_filepath, pdf_filepath)

    return pdf_filepath
