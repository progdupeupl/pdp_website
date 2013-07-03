# README

Progdupeupl is a community of French programmers ; you can see the running
version [here](http://progdupeu.pl/).

## Naming conventions

Everything in the code should be in english (vars, funcs, methods, docstrings,
comments) though some parts may - of course - be in French. PEP-8 is good too.

## Dependencies

To install all Python 2 dependencies, simply run
`pip install -r requirements.txt`.

Moreover, in order to generate the
CSS files with included Makefile, you will need to install
[Compass](http://compass-style.org) and [Zurb Foundation](http://foundation.zurb.com/)' ruby gems
using `gem install compass zurb-foundation`.

## Deployment

From the project's root, you will need to run the following commands:

    python manage.py syncdb
    python manage.py migrate

And finally, the CSS must be generated from the SASS sources, using the Makefile located in the `assets` directory.

## Copyright

Progdupeupl is brought to you under GNU GPLv3 licence. For further informations
read the COPYING file. This project use some code parts from
[progmod](http://progmod.org) avaible under the MIT licence.
