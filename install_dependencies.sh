#!/bin/bash

# Note: we must use Bash over POSIX Shell here because of the "source" command
# allowing use to switch inside the virtualenv once created.
#
# This is the only reason why bash is kept here instead of sh. Rest of the
# script should be POSIX compatible.

# Check for Rubygems
gempath=$(which gem)
if [ ! -f "$gempath" ]; then
	echo "You need to install the Ruby `gem` package manager"
	exit 1
fi

# Check for Python virtualenv tool
venvpath=$(which virtualenv)
if [ ! -f "$venvpath" ]; then
	echo "You need to install Python 3 virtualenv tool"
	exit 2
fi

# Check if the C compiler is GCC
#
# This check is performed because the C Python packages this project rely on
# will fail to compile using the well-known Clang compiler ATM.
if [ "$CC" != "gcc" ]; then
	echo "You must use GCC to install the Python dependencies, please fix" \
		"your \$CC environment variable."
	echo "Current \$CC value is : $CC"
	exit 3
fi

# Install gems
echo "Installing Ruby dependencies..."
gem install --user-install compass sass zurb-foundation

# Create virtualenv
echo "Creating Python 3 virtualenv..."
if [ ! -d venv ]; then
	virtualenv --python=python3 venv
fi
source venv/bin/activate

# Installing Python dependencies in virtualenv
echo "Installing Python dependencies inside the virtualenv..."
pip install -r requirements.txt && echo "Successfully installed PDP dependencies!"
