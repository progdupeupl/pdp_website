#!/bin/bash

# Check for Rubygems
gempath=$(which gem)
if [ ! -f "$gempath" ]; then
	echo "You need to install the Ruby `gem` package manager"
fi

# Check for Python virtualenv
venvpath=$(which virtualenv)
if [ ! -f "$venvpath" ]; then
	echo "You need to install Python 3 virtualenv tool"
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
