#!/bin/bash

function checkExecutable {
	echo -ne "Looking for executable $1 in PATH..."
	local path=$(which $1)
	if [ -f "$path" ]; then
		echo -e " found $path"
	else
		exit 1
	fi
}


checkExecutable sass
checkExecutable compass
