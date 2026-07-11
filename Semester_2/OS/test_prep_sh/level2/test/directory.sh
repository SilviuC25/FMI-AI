#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Error: a directory name is needed as parameter"
	exit 1
fi

if [ ! -d "$1" ]; then
	echo "The given name is not a directory"
else 
	echo "The given name is a directory"
fi
