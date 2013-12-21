# coding: utf-8

"""A small module for handling some common operations on articles."""

from collections import OrderedDict

from pdp.utils.schemas import validate_article

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
