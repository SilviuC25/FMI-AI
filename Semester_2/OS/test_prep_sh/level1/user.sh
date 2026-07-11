#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Error: User must be given as a parameter"
	exit 1
fi

if who | grep -q -w "^$1"; then
	echo "User connected"
else 
	echo "User not connected"
fi

