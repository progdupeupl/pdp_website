# Progdupeupl’s website

Progdupeupl (PDP) is a community of French programmers and this website is its
main medium. You can see the running version [here](http://pdp.microjoe.org/).

## Language convention

The site being in French, user-interface strings are in french − there is no
localization yet. However, to let others reuse our code, everything in the code
should be in english (vars, funcs, methods, docstrings, comments, commits,
everything!), and we'd rather interact in english for development (bug reports,
pull requests, etc.).

As for other style matters in the code, the [PEP-8 Style
Guide](http://www.python.org/dev/peps/pep-0008/) is a good base for the Python
source code of this project.

## Dependencies

Progdupeupl (PDP) uses [Django](https://www.djangoproject.com/), a web
framework for the [Python](http://python.org/) programming language (we only
support Python 3 now), but it also uses tools implemented in
[Ruby](https://www.ruby-lang.org/en/).

You must have at least recent-enough versions of Python 3 (at least 3.3) and
Ruby installed on your system, and installation instructions will depend on
your operating system. Once you've set up those base dependencies, additional
packages are installed through language-specific package managers which should
work similarly on all systems.

### Basic dependencies (system-dependent)

You should install Python 3.3 or 3.4, and the
[pip](http://www.pip-installer.org/en/latest/) package manager. Under
Debian/Ubuntu systems for example, you can use the following commands:

    # apt-get install python3.3 python3.3-dev
    # apt-get install python3-pip
    # apt-get install python-virtualenv

You will also need Ruby, that on most systems come with its own package manager
`gem`. Again on Debian/Ubuntu:

    # aptitude install ruby

To run Ruby gem executables, you will need to add the Ruby gem
executable directory to your `$PATH`:

    export PATH=$PATH:$(ruby -rubygems -e "puts Gem.user_dir")/bin

Which you can put in your `.bashrc` or `.zshrc` for convenience.

### Libraries and tools (system-independent)

Once basic system packages have been installed, you can run the automatic
bootstrap script which will create a virtualenv for you and install all Python
and Ruby dependencies.

    $ make bootstrap

If the bootstrap script fails, the error should appear in the build messages
(like missing "Python.h" if you forgot to install `python3-dev`). Try to fix
the error and run the bootstrap make target again.

## First run

The boostrap target also have created a test database filled with example data
and generated the search engine index for it. You are ready to go!

**You can login with these dummy users using their lowercase usernames as their
respective passwords**.

You are ready to run a test server on your local machine:

    $ # activate the virtual environment (no need to repeat this in a given session)
    $ source venv/bin/activate
    $ # run the server
    (venv)$ python manage.py runserver

The test instance should be available at
[http://localhost:8000](http://localhost:8000). It will automatically update its
behavior if you edit the code of the project. Enjoy, and send us lots of good
patches!

If you are very new to how virtualenv works or have a problem with virtualenv,
please read the `virtualenv.md` file in order to get some help.

## Running background tasks

In order to generate PDF files using a background task scheduler named celery,
you will need to start it. A shortcut is provided in the Makefile, simply
type:

    $ make celery

And the celery server will start. You will also need Pandoc as PDF generator
from Markdown sources.

## Updating the local data after schema change

If you add new fields to a `models.py` source file, Python will complain that
the database schema is out-of-date. To fix this, perform a schema migration
using the two following commands, replacing `forum` in the line `APP=forum`
with the subdirectory of `pdp` in which you made the modifications (article,
forum, gallery, member, messages, pages, tutorial, utils…):

    (venv)$ APP=forum
    (venv)$ python manage.py schemamigration pdp.$APP --auto
    (venv)$ python manage.py migrate $APP

## Documentation

If you want to build the documentation, you will need to install Sphinx 1.3 for
its support of Google docstrings format. This version is now available in PyPI
so you can install it using `pip install sphinx`.

Then, go in the `doc/` directory and type `make html` to generate the HTML
documentation of the project (mainly classes/functions documentation at the
moment but this may improve in the future).

## Copyright

Progdupeupl is brought to you under [GNU Affero General Public Licence version
3+](http://www.gnu.org/licenses/agpl-3.0.html). For further informations please
read the provided LICENSE file.
