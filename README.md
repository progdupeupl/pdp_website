# Progdupeupl

Progdupeupl is a community of French programmers ; you can see the running
version [here](http://progdupeu.pl/).

## Language convention

The site being in French, user-interface strings are in french --
there is no localization yet. However, to let others reuse our code,
everything in the code should be in english (vars, funcs, methods,
docstrings, comments), and we'd rather interact in english for
development (bug reports, pull requests, etc.).

As for other style matters in the code, the [PEP-8 Style
Guide](http://www.python.org/dev/peps/pep-0008/) is a good base.

## Dependencies

To install all Python 2 dependencies, simply run
`pip install -r requirements.txt`.

Moreover, in order to generate the CSS files with included Makefile, you will
need to install [Compass](http://compass-style.org) and [Zurb
Foundation](http://foundation.zurb.com/)' ruby gems using `gem install compass
zurb-foundation`.

Finally, if you want to navigate in `debug = False` mode then you will need to
have `yuglify` on your system in order to compress CSS and JS sheets.

## Deployment

From the project's root, you will need to run the following command:

    :::console
    fab bootstrap

Once everything is synced, you will have to create a Profile instance for
your superuser account using the your credentials and the Django admin system
aivaible on `/admin/`.

## Copyright

Progdupeupl is brought to you under GNU GPLv3 licence. For further informations
read the COPYING file. This project use some code parts from
[progmod](http://progmod.org) available under the MIT licence.
