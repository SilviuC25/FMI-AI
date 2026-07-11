#!/bin/bash

if [ $# -eq 0 ]; then
	echo "Use a folder path as parameter"
	exit 1
fi

FOLDER_PATH=$1

if [ ! -d "$FOLDER_PATH" ]; then
	echo "Error: '$FOLDER_PATH' is not a valid directory"
	exit 1;
fi

echo "The total size of the folder is: "
du -sh "$FOLDER_PATH"
