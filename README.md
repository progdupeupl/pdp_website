# Progdupeupl

Progdupeupl (PDP) is a community of French programmers ; you can see the
running version [here](http://progdupeu.pl/).

## Language convention

The site being in French, user-interface strings are in french -- there is no
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
[node.js](http://nodejs.org/) javascript framework.

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
    sudo aptitude install python2.7
    sudo aptitude install python-pip

You will also need Ruby, that on most systems come with its own package manager
`gem`. Again on Debian/Ubuntu:

    :::console
    sudo aptitude install ruby

Installing Node.js and its [npm](https://npmjs.org/) package manager is
optional, it is only needed if you want to run PDP in mode `debug = False`
(with minified sources). You do not need it for development purposes.

    :::console
    sudo aptitude install npm

### Libraries and tools (system-independent)

All the python dependencies for PDP are listed in the file `requirements.txt`
in the source repository. From the PDP directory, simply run

    :::console
    pip install --user -r requirements.txt

(This will install the full Django framework and a few separate modules, so it
may take some time.)

Moreover, we use the Ruby programs [Compass](http://compass-style.org) and
[Zurb Foundation](http://foundation.zurb.com/) to generate CSS files. You can
install them with the `gem` package manager distributed with Ruby:

    :::console
    gem install --user-install compass zurb-foundation

Finally, if you want to navigate in mode `debug = False`, then you will need to
have [yuglify](https://github.com/yui/yuglify) on your system in order to
compress CSS and JS sheets.

    :::console
    npm install yuglify

## Deployment

From the project's root, you will need to run the following command, which uses
the build and deployment tool [Fabric](http://docs.fabfile.org/en/1.8/).

    :::console
    fab bootstrap

Once everything is synced, you will have to create a Profile instance for your
superuser account using the your credentials and the Django admin system
aivaible on `/admin/`.

You can then create run a test server on your local machine:

    :::console
    python manage.py runserver

The test instance should be available at
[http://localhost:8000](http://localhost:8000). It will automatically update its
behavior if you edit the code of the project. Enjoy, and send us lots of good
patches!

## Copyright

Progdupeupl is brought to you under GNU GPLv3 licence. For further informations
read the COPYING file. This project use some code parts from
[progmod](http://progmod.org) available under the MIT licence.
