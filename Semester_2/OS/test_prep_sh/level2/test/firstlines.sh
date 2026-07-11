#!/bin/bash

for DIR in $@; do
	if [ ! -d "$DIR" ]; then
		echo "Error: '$DIR' is not a directory"
		exit 1
	fi
	for FILE in "$DIR"/*; do
		echo "File '$FILE':"
		head -n "$FILE"
	done
done
