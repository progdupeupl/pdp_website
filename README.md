# Progdupeupl

Progdupeupl (PDP) is a community of French programmers ; you can see the
running version [here](http://progdupeu.pl/).

[![Build Status](https://api.shippable.com/projects/540f4bef5adf368bc3901fc7/badge?branchName=master)](https://app.shippable.com/projects/540f4bef5adf368bc3901fc7/builds/latest)

## Language convention

The site being in French, user-interface strings are in french − there is no
localization yet. However, to let others reuse our code, everything in the code
should be in english (vars, funcs, methods, docstrings, comments), and we'd
rather interact in english for development (bug reports, pull requests, etc.).

As for other style matters in the code, the [PEP-8 Style
Guide](http://www.python.org/dev/peps/pep-0008/) is a good base.


## Dependencies

Progdupeupl (PDP) uses [Django](https://www.djangoproject.com/), a web
framework for the [Python](http://python.org/) programming language (we only
support Python 3 now), but it also uses tools implemented in
[Ruby](https://www.ruby-lang.org/en/), and (optionally) with the
[Node.js](http://nodejs.org/) Javascript framework.

You must have at least recent-enough versions of Python 3 (at least 3.3) and
Ruby installed on your system, and installation instructions will depend on
your operating system. Once you've set up those base dependencies, additional
packages are installed through language-specific package managers which should
work similarly on all
systems.

### Basic dependencies (system-dependent)

You should install Python 3.3 or 3.4, and the
[pip](http://www.pip-installer.org/en/latest/) package manager. Under
Debian/Ubuntu systems for example, you can use the following commands:

    :::console
    # aptitude install python3.3 python3.3-dev
    # aptitude install python3-pip

You will also need Ruby, that on most systems come with its own package manager
`gem`. Again on Debian/Ubuntu:

    :::console
    # aptitude install ruby

Installing Node.js and its [npm](https://npmjs.org/) package manager is
optional, it is only needed if you want to run PDP in mode `debug = False`
(with minified sources). You do not need it for development purposes.

    :::console
    # aptitude install npm

### Virtual python environment (virtualenv)

The `virtualenv` tool is designed to avoid problem with incompatible Python
versions or conflicting package requirements between distinct projects. It
allows to set up per-project local environments, setting a preferred version of
Python, and installing dependencies locally. To install `virtualenv`, simply
run

    :::console
    $ pip3 install --user virtualenv

If you are in the `progdupeupl` directory, you can then create a local
environment in a new subdirectory `venv`, asking it to use the `python3`
executable; if the Python 3 interpreter is named differently on your system,
eg. `python3.3` or `python`, you should change the name.

    :::console
    $ virtualenv --python=python3 --distribute venv

Each time you want to work on PDP, you should go to the `progdupeupl` directory
and "activate" this virtual environment. Once the environment is activated, all
Python tools will use it; for example they will use the `python2` interpreter
even if your operating system uses Python 2 by default. This will avoid you
a lot of annoying version mismatches.

    :::console
    $ source venv/bin/activate

Do this now before installing further Python dependencies.

You can check that the environment has been activated correctly by printing the
`$VIRTUAL_ENV` environment variable, and de-activate the environment to get back
to your default Python system by just running the `deactivate` command.

### Libraries and tools (system-independent)

All the python dependencies for PDP are listed in the file `requirements.txt`
in the source repository. From the PDP directory, simply run

    :::console
    (venv)$ pip install -r requirements.txt

(This will install the full Django framework and a few separate modules, so it
may take some time.)

Since South is not supporting Python 3 for its last release you will have to
install the current dev version:

    :::console
    (venv)$ hg clone https://bitbucket.org/andrewgodwin/south
    ...
    (venv)$ pip install ./south/

Moreover, we use the Ruby programs [Compass](http://compass-style.org) and
[Zurb Foundation](http://foundation.zurb.com/) to generate CSS files. You can
install them with the `gem` package manager distributed with Ruby:

    :::console
    $ gem install --user-install compass zurb-foundation

To run compass and zurb-foundation, you will need to add `~/.gem/ruby/1.9.1/bin`
to your `$PATH`.

Finally, if you want to navigate in mode `debug = False`, then you will need to
have [yuglify](https://github.com/yui/yuglify) on your system in order to
compress CSS and JS sheets.

    :::console
    $ npm install yuglify

## First run

From the project's root, you will need to run the following Make target:

    :::console
    (venv)$ make bootstrap

Once everything is synced, you can then run a test server on your local
machine:

    :::console
    $ # activate the virtual environment (no need to repeat this in a given session)
    $ source venv/bin/activate
    $ # run the server
    (venv)$ python manage.py runserver

The test instance should be available at
[http://localhost:8000](http://localhost:8000). It will automatically update its
behavior if you edit the code of the project. Enjoy, and send us lots of good
patches!

## Running background tasks

In order to generate PDF files using a background task scheduler named celery,
you will need to start it. A shortcut is provided in the Makefile, simply
type:

    :::console
    $ make celery

And the celery server will start. You will also need Pandoc as PDF generator
from Markdown sources.

## Filling your local database with data

If you want to fill the database with fake data, you can import them from
fixtures. You only have to run this command:

    :::console
    (venv)$ make loadfixtures

It will create:

 - the forums' and tutorials' categories.
 - 6 users and their profiles.
 - 2 topics with 3 posts on each one.
 - 1 private message.

You can login with these dummy users using their lowercase usernames as their
respective passwords.

## Updating the local data after schema change

If you add new fields to a models.py, Python will complain that the
database schema is out-of-date. To fix this, perform a schema
migration using the two following commands, replacing `forum` in the
line `APP=forum` with the subdirectory of `pdp` in which you made the
modifications (article, forum, gallery, member, messages, pages,
tutorial, utils...):

    :::console
    (venv)$ APP=forum
    (venv)$ python manage.py schemamigration pdp.$APP --auto
    (venv)$ python manage.py migrate $APP

## Documentation

If you want to build the documentation, you will need to install Sphinx 1.3 for
its support of Google docstrings format. Since this version is 'till not
released, you will have to [manually download a Sphinx snapshot on their
website](http://sphinx-doc.org/install.html), uncompress it and and tell PIP to
install it from local folder:

    :::console
    (venv)$ pip install ~/tmp/birkenfeld-sphinx-xxxxxxxxxxxx/

Then, you need to set an environment variable in your shell in order to make
the documentation generation work (because of Django's settings handling) and
run the makefile :

    :::console
    (venv)$ cd doc/
    (venv)$ export DJANGO_SETTINGS_MODULE=pdp.settings
    (venv)$ make html

## Copyright

Progdupeupl is brought to you under [GNU Affero General Public Licence version
3+](http://www.gnu.org/licenses/agpl-3.0.html). For further informations please
read the COPYING file.