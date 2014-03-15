# coding: utf-8
#
# This file is part of Progdupeupl.
#
# Progdupeupl is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Progdupeupl is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Progdupeupl. If not, see <http://www.gnu.org/licenses/>.

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
