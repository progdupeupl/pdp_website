# Progdupeupl

Progdupeupl is a community of French programmers ; you can see the running
version [here](http://progdupeu.pl/).

## Naming conventions

Everything in the code should be in english (vars, funcs, methods, docstrings,
comments) though some parts may - of course - be in French. PEP-8 is good too.

## Dependencies

To install all Python 2 dependencies, simply run
`pip install -r requirements.txt`.

Moreover, in order to generate the CSS files with included Makefile, you will
need to install [Compass](http://compass-style.org) and [Zurb
Foundation](http://foundation.zurb.com/)' ruby gems using `gem install compass
zurb-foundation`.

## Deployment

From the project's root, you will need to run the following command:

    :::console
    fab bootstrap

Once everything is synced, you will have to create a Profile instance for
your superuser account using the your credentials and the Django admin system
aivaible on `/admin/`.

If you want to start with example data, you can execute the following command
after creating the database : `python manage.py loaddata data.json`.

## Copyright

Progdupeupl is brought to you under GNU GPLv3 licence. For further informations
read the COPYING file. This project use some code parts from
[progmod](http://progmod.org) available under the MIT licence.
