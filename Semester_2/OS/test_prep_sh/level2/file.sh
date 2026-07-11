#!/bin/bash

if [ ! $# -gt 1 ]; then
	echo "Error: one or more filenames are needed"
	exit 1
fi

for filename in "$@"; do
	if [ ! -f "$filename" ]; then
		echo "Error: $filename is not a file"
		continue
	fi
	lines=$(wc -l < $filename)
	echo "$filename has $lines lines"
done


