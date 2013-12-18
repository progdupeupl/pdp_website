# coding: utf-8

"""Module handling schema validation support for items."""

import json
import jsonschema

# Defining constants

ARTICLE_SCHEMA = 'assets/schemas/article.json'
TUTORIAL_SCHEMA = 'assets/schemas/tutorial.json'


# General functions

def validate_from_schema(schema, dct):
    """Validate a dictionnary based on a specific schema.

    Args:
        schema: dictionnary containing the schema
        dct: dictionnary to validate

    Returns:
        True if validation was possible and successfully passed.

    """

    try:
        jsonschema.validate(dct, schema)
    except jsonschema.RefResolutionError:
        # Foreign $ref schema not found, so we can't continue validation in
        # deeper levels.
        return False
    except jsonschema.ValidationError:
        # Validation failed.
        return False

    # No exception raised, validation passed!
    return True


def validate_from_file(filepath, dct):
    """Validate a dictionnary based on a specific schema described in a file.

    Args:
        filepath: path to the JSON file containing the schema
        dct: dictionnary to validate

    Returns:
        True if validation was possible and successfully passed.

    """

    with open(filepath) as f:
        schema = json.load(f)

    return validate_from_schema(schema, dct)


# Specific functions

def validate_article(dct):
    """Validate a dictionnary representing article data.

    Args:
        dct: dictionnary representing the article

    Returns:
        True if validation was possible and successfully passed.

    """
    return validate_from_file(ARTICLE_SCHEMA, dct)


def validate_tutorial(dct):
    """Validate a dictionnary representing tutorial data.

    Args:
        dct: dictionnary representing the tutorial

    Returns:
        True if validation was possible and successfully passed.

    """
    return validate_from_file(TUTORIAL_SCHEMA, dct)
