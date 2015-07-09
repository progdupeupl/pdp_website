# Using a virtual python environment (virtualenv) with PDP

The `virtualenv` tool is designed to avoid problem with incompatible Python
versions or conflicting package requirements between distinct projects. It
allows to set up per-project local environments, setting a preferred version of
Python, and installing dependencies locally. To install `virtualenv`, simply
run

    $ pip3 install --user virtualenv

If you are in the `progdupeupl` directory, you can then create a local
environment in a new subdirectory `venv`, asking it to use the `python3`
executable; if the Python 3 interpreter is named differently on your system,
eg. `python3.3` or `python`, you should change the name.

    $ virtualenv --python=python3 venv

Each time you want to work on PDP, you should go to the `progdupeupl` directory
and "activate" this virtual environment. Once the environment is activated, all
Python tools will use it; for example they will use the `python3` interpreter
even if your operating system uses Python 2 by default. This will avoid you
a lot of annoying version mismatches.

    $ source venv/bin/activate

Do this now before installing further Python dependencies.

You can check that the environment has been activated correctly by printing the
`$VIRTUAL_ENV` environment variable, and de-activate the environment to get
back to your default Python system by just running the `deactivate` command.
