# Progdupeupl

Progdupeupl (PDP) is a community of French programmers ; you can see the
running version [here](http://progdupeu.pl/).

## Language convention

The site being in French, user-interface strings are in french − there is no
localization yet. However, to let others reuse our code, everything in the code
should be in english (vars, funcs, methods, docstrings, comments), and we'd
rather interact in english for development (bug reports, pull requests, etc.).

As for other style matters in the code, the [PEP-8 Style
Guide](http://www.python.org/dev/peps/pep-0008/) is a good base.


## Dependencies

Progdupeupl (PDP) uses [Django](https://www.djangoproject.com/), a web
framework for the [Python](http://python.org/) programming language (we
currently only support Python 2, not Python 3), but it also uses tools
implemented in [Ruby](https://www.ruby-lang.org/en/), and (optionally) with the
[Node.js](http://nodejs.org/) Javascript framework.

You must have at least recent-enough versions of Python 2 (at least 2.6) and
Ruby installed on your system, and installation instructions will depend on
your operating system. Once you've set up those base dependencies, additional
packages are installed through language-specific package managers which should
work similarly on all
systems.

### Basic dependencies (system-dependent)

You should install Python 2.6 or 2.7, and the
[pip](http://www.pip-installer.org/en/latest/) package manager. Under
Debian/Ubuntu systems for example, you can use the following commands:

    :::console
    # aptitude install python2.7 python2.7-dev
    # aptitude install python-pip

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
    $ pip install --user virtualenv

If you are in the `progdupeupl` directory, you can then create a local
environment in a new subdirectory `venv`, asking it to use the `python2`
executable; if the Python 2 interpreter is named differently on your system,
eg. `python2.7` or `python`, you should change the name.

    :::console
    $ virtualenv --python=python2 --distribute venv

Each time you want to work on PDP, you should go to the `progdupeupl` directory
and "activate" this virtual environment. Once the environment is activated, all
Python tools will use it; for example they will use the `python2` interpreter
even if your operating system uses Python 3 by default. This will avoid you
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

In order to generate PDF files using a background task scheduler named celery,
you will need to start it. A shortcut is provided in the fabfile, simply type :

    :::console
    $ fab celery

And the celery server will start. You will also need Pandoc as PDF generator
from Markdown sources.

## Deployment

From the project's root, you will need to run the following command, which uses
the build and deployment tool [Fabric](http://docs.fabfile.org/en/1.8/).

    :::console
    (venv)$ fab bootstrap

Once everything is synced, you will have to create a Profile instance for your
superuser account using the your credentials and the Django admin system
aivaible on `/admin/`.

You can then create run a test server on your local machine:

    :::console
    $ # activate the virtual environment (no need to repeat this in a given session)
    $ source venv/bin/activate
    $ # run the server
    $ python manage.py runserver

The test instance should be available at
[http://localhost:8000](http://localhost:8000). It will automatically update its
behavior if you edit the code of the project. Enjoy, and send us lots of good
patches!

## Documentation

If you want to build the documentation, you will need to install Sphinx 1.3 for
its support of Google docstrings format. Since this version is 'till not
released, you can install latest version of Sphinx using pip :

    :::console
    $ pip install sphinx==dev

Then, you need to set an environment variable in your shell in order to make
the documentation generation work, because of Django's settings handling :

    :::console
    $ cd doc
    $ export DJANGO_SETTINGS_MODULE=pdp.settings
    $ make html

## Copyright

Progdupeupl is brought to you under GNU GPLv3 licence. For further informations
read the COPYING file. This project use some code parts from
[progmod](http://progmod.org) available under the MIT licence.
