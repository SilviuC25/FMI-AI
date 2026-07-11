#!/bin/bash

if [ $# -ne 2 ]; then
	echo "Error: 2 parameters needed - text file and output folder"
	exit 1
fi

FILE=$1
OUTPUT=$2

if [ ! -f "$FILE" ]; then
	echo "Error: first parameter needs to be a textfile"
	exit 1
fi

if [ ! -d "$OUTPUT" ]; then
	echo "Error: second parameter needs to be a directory"
	exit 1
fi


WORDS=$(cat "$FILE" | tr "A-Z" "a-z" | sort -u)

for LETTER in {a..z}; do
	DICT_FILE="$OUTPUT/${LETTER}.dict"

	echo "$WORDS" | grep "^$LETTER" > "$DICT_FILE"
done
